# *_*coding:utf-8 *_*
# @Author : YueMengRui
import os
import json
import time
import base64
import shutil
import requests
from io import BytesIO
from PIL import Image
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends
from info.utils.Authentication import verify_token
from info import logger, limiter, get_mysql_db
from configs import API_LIMIT, QWENVL_CHAT, TEMP, UPLOAD_FILE_URL
from .protocol import ErrorResponse, ChatVLRequest, ChatVLImageRequest
from fastapi.responses import JSONResponse, StreamingResponse
from info.mysql_models import ChatMessageRecord, ChatRecord
from info.utils.response_code import RET, error_map

router = APIRouter()


@router.api_route('/ai/llm/chat/vl/image', methods=['POST'], summary="Chat")
@limiter.limit(API_LIMIT['chat'])
def llm_chat_vl_image(request: Request,
                      req: ChatVLImageRequest,
                      mysql_db: Session = Depends(get_mysql_db),
                      user_id=Depends(verify_token)
                      ):
    logger.info(str(req.dict()) + ' user_id: {}'.format(user_id))

    new_message_user = ChatMessageRecord()
    new_message_user.chat_id = req.chat_id
    new_message_user.uid = req.uid
    new_message_user.role = 'user'
    new_message_user.type = 'image'
    new_message_user.url = req.url
    new_message_user.llm_name = req.model_name

    try:
        mysql_db.add(new_message_user)
        mysql_db.commit()
    except Exception as e:
        logger.error({'DB ERROR': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    return JSONResponse({'msg': 'success'})


@router.api_route('/ai/llm/chat/vl', methods=['POST'], summary="Chat")
@limiter.limit(API_LIMIT['chat'])
def llm_chat_vl(request: Request,
                req: ChatVLRequest,
                mysql_db: Session = Depends(get_mysql_db),
                user_id=Depends(verify_token)
                ):
    logger.info(str(req.dict()) + ' user_id: {}'.format(user_id))

    start = time.time()
    new_message_user = ChatMessageRecord()
    new_message_user.chat_id = req.chat_id
    new_message_user.uid = req.uid
    new_message_user.role = 'user'
    new_message_user.content = str(req.prompt)
    new_message_user.llm_name = req.model_name

    chat = mysql_db.query(ChatRecord).get(req.chat_id)
    if not chat.name:
        chat.dynamic_name = req.prompt[:8]

    try:
        mysql_db.add(new_message_user)
        mysql_db.commit()
    except Exception as e:
        logger.error({'DB ERROR': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    logger.info(f"prompt: {req.true_prompt}")
    req_data = {
        "model_name": req.model_name,
        "prompt": req.true_prompt,
        "history": req.history,
        "generation_configs": req.generation_configs,
        "stream": False
    }
    if req.stream:
        req_data.update({"stream": True})
        resp = requests.post(url=QWENVL_CHAT, json=req_data, stream=True)
        if 'event-stream' in resp.headers.get('content-type'):
            def stream_generate():
                for line in resp.iter_content(chunk_size=None):
                    res = json.loads(line.decode('utf-8'))
                    res['time_cost'].update({'total': f"{time.time() - start:.3f}s"})
                    if res['type'] == "image":
                        image_url = upload_file(res['image'])
                        res.pop('image')
                        res.update({'url': image_url})

                    yield f"data: {json.dumps(res, ensure_ascii=False)}\n\n"

                new_message_assistant = ChatMessageRecord()
                new_message_assistant.chat_id = req.chat_id
                new_message_assistant.uid = req.answer_uid
                new_message_assistant.role = 'assistant'
                if res['type'] == 'image':
                    new_message_assistant.type = 'image'
                    new_message_assistant.url = res['url']
                else:
                    new_message_assistant.content = res['answer']
                new_message_assistant.llm_name = res['model_name']
                new_message_assistant.response = res

                mysql_db.add(new_message_assistant)

                try:
                    mysql_db.commit()
                except Exception as e:
                    logger.error({'DB ERROR': e})
                    mysql_db.rollback()

            return StreamingResponse(stream_generate(), media_type="text/event-stream")
        else:
            return JSONResponse(resp.json())

    else:
        resp = requests.post(url=QWENVL_CHAT, json=req_data).json()
        resp['time_cost'].update({'total': f"{time.time() - start:.3f}s"})

        new_message_assistant = ChatMessageRecord()
        new_message_assistant.chat_id = req.chat_id
        new_message_assistant.uid = req.answer_uid
        new_message_assistant.role = 'assistant'
        new_message_assistant.content = resp['answer']
        new_message_assistant.llm_name = resp['model_name']
        new_message_assistant.response = resp

        mysql_db.add(new_message_assistant)

        try:
            mysql_db.commit()
        except Exception as e:
            logger.error({'DB ERROR': e})
            mysql_db.rollback()
            return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)
        return JSONResponse(resp)


def upload_file(base64_str):
    # image_bytes = BytesIO(base64.b64decode(base64_str.encode('utf-8')))

    image = base64.b64decode(base64_str.encode('utf-8'))
    image = BytesIO(image)
    image = Image.open(image)
    file_name = str(time.time() * 1000000) + '.jpg'
    temp_path = os.path.join(TEMP, file_name)
    image.save(temp_path)
    resp = requests.post(url=UPLOAD_FILE_URL,
                         files={"file": (file_name, open(temp_path, 'rb'))})
    logger.info(resp.text)
    shutil.rmtree(temp_path, ignore_errors=True)
    return resp.json()['file_url']


def base64_pil(base64_str: str):
    image = base64.b64decode(base64_str.encode('utf-8'))
    image = BytesIO(image)
    image = Image.open(image)
    return image
