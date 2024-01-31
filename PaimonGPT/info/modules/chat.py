# *_*coding:utf-8 *_*
# @Author : YueMengRui
import json
import time
import requests
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends
from info.utils.Authentication import verify_token
from info import logger, limiter, get_mysql_db, LLM_Models
from configs import API_LIMIT, LLM_SERVER_APIS
from .protocol import ChatRequest, TokenCountRequest, ErrorResponse, ChatSimpleRequest
from fastapi.responses import JSONResponse, StreamingResponse
from info.mysql_models import ChatMessageRecord, ChatRecord
from info.utils.response_code import RET, error_map
from info.utils.kb.prompt_handler import get_final_prompt
from info.utils.api_servers.llm_base import servers_token_count

router = APIRouter()


@router.api_route(path='/ai/llm/list', methods=['GET'], summary="获取支持的llm列表")
@limiter.limit(API_LIMIT['model_list'])
def support_llm_list(request: Request,
                     user_id=Depends(verify_token)
                     ):
    return JSONResponse({'data': [{'model_name': k, **v['info']} for k, v in LLM_Models.items()]})


@router.api_route('/ai/llm/chat', methods=['POST'], summary="Chat")
@limiter.limit(API_LIMIT['chat'])
def llm_chat(request: Request,
             req: ChatRequest,
             mysql_db: Session = Depends(get_mysql_db),
             user_id=Depends(verify_token)
             ):
    logger.info(str(req.dict()) + ' user_id: {}'.format(user_id))
    start = time.time()
    new_message_user = ChatMessageRecord()
    new_message_user.chat_id = req.chat_id
    new_message_user.uid = req.uid
    new_message_user.role = 'user'
    new_message_user.content = req.prompt
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

    prompt, related_docs, msg = get_final_prompt(req=req, app_id=req.app_id, mysql_db=mysql_db)
    logger.info(f"prompt: {prompt}")
    req_data = {
        "model_name": req.model_name,
        "prompt": prompt,
        "history": req.history,
        "generation_configs": req.generation_configs,
        "stream": False
    }
    if req.stream:
        req_data.update({"stream": True})
        resp = requests.post(url=LLM_Models[req.model_name]['url_prefix'] + LLM_SERVER_APIS['chat'], json=req_data,
                             stream=True)
        if 'event-stream' in resp.headers.get('content-type'):
            def stream_generate():
                for line in resp.iter_content(chunk_size=None):
                    res = json.loads(line.decode('utf-8'))
                    res['time_cost'].update({'total': f"{time.time() - start:.3f}s"})
                    retrieval = {}
                    retrieval.update({'sources': related_docs})
                    retrieval.update({'sources_len': sum([len(x['related_content']) for x in related_docs])})
                    retrieval.update(msg)
                    res.update({'retrieval': retrieval})
                    yield f"data: {json.dumps(res, ensure_ascii=False)}\n\n"

                new_message_assistant = ChatMessageRecord()
                new_message_assistant.chat_id = req.chat_id
                new_message_assistant.uid = req.answer_uid
                new_message_assistant.role = 'assistant'
                new_message_assistant.content = res['answer']
                new_message_assistant.llm_name = res['model_name']
                new_message_assistant.response = res
                if 'MultiQueryRetriever' in msg:
                    new_message_assistant.is_multiQueryRetriever_enabled = True

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
        resp = requests.post(url=LLM_Models[req.model_name]['url_prefix'] + LLM_SERVER_APIS['chat'],
                             json=req_data).json()
        resp['time_cost'].update({'total': f"{time.time() - start:.3f}s"})
        retrieval = {}
        retrieval.update({'sources': related_docs})
        retrieval.update({'sources_len': sum([len(x['related_content']) for x in related_docs])})
        retrieval.update(msg)
        resp.update({'retrieval': retrieval})

        new_message_assistant = ChatMessageRecord()
        new_message_assistant.chat_id = req.chat_id
        new_message_assistant.uid = req.answer_uid
        new_message_assistant.role = 'assistant'
        new_message_assistant.content = resp['answer']
        new_message_assistant.llm_name = resp['model_name']
        new_message_assistant.response = resp
        if 'MultiQueryRetriever' in msg:
            new_message_assistant.is_multiQueryRetriever_enabled = True

        mysql_db.add(new_message_assistant)

        try:
            mysql_db.commit()
        except Exception as e:
            logger.error({'DB ERROR': e})
            mysql_db.rollback()
            return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)
        return JSONResponse(resp)


@router.api_route('/ai/llm/token_count', methods=['POST'], summary="token count")
@limiter.limit(API_LIMIT['token_count'])
def count_token(request: Request,
                req: TokenCountRequest,
                user_id=Depends(verify_token)
                ):
    logger.info(str(req.dict()))

    return JSONResponse(servers_token_count(**req.dict()).json())


@router.api_route('/ai/llm/chat/simple', methods=['POST'], summary="Chat Simple")
@limiter.limit(API_LIMIT['chat'])
def llm_chat_simple(request: Request,
                    req: ChatSimpleRequest,
                    user_id=Depends(verify_token)
                    ):
    start = time.time()
    logger.info(str(req.dict()))

    req_data = {
        "model_name": req.model_name,
        "prompt": req.prompt,
        "history": req.history,
        "generation_configs": req.generation_configs,
        "stream": False
    }
    if req.stream:
        req_data.update({"stream": True})
        resp = requests.post(url=LLM_Models[req.model_name]['url_prefix'] + LLM_SERVER_APIS['chat'], json=req_data,
                             stream=True)
        if 'event-stream' in resp.headers.get('content-type'):
            def stream_generate():
                for line in resp.iter_content(chunk_size=None):
                    res = json.loads(line.decode('utf-8'))
                    res['time_cost'].update({'total': f"{time.time() - start:.3f}s"})
                    yield f"data: {json.dumps(res, ensure_ascii=False)}\n\n"

            return StreamingResponse(stream_generate(), media_type="text/event-stream")
        else:
            return JSONResponse(resp.json())

    else:
        resp = requests.post(url=LLM_Models[req.model_name]['url_prefix'] + LLM_SERVER_APIS['chat'],
                             json=req_data).json()
        resp['time_cost'].update({'total': f"{time.time() - start:.3f}s"})

        return JSONResponse(resp)
