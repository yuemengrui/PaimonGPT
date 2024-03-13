# *_*coding:utf-8 *_*
# @Author : YueMengRui
import time
import requests
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends
from info.utils.Authentication import verify_token
from info import logger, limiter, get_mysql_db
from configs import API_LIMIT, LLM_SERVER_APIS, LLM_SERVER_PREFIX
from configs.prompt_template import MERMAID_PROMPT_TEMPLATE
from .protocol import ChatRequest, ErrorResponse
from fastapi.responses import JSONResponse
from info.mysql_models import ChatMessageRecord, ChatRecord
from info.utils.response_code import RET, error_map
from info.utils.parse_str_to_mermaid import parse_str_to_mermaid

router = APIRouter()


@router.api_route('/ai/llm/chat/chart', methods=['POST'], summary="Chart Chat")
@limiter.limit(API_LIMIT['chat'])
def llm_chat_chart(request: Request,
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

    prompt = MERMAID_PROMPT_TEMPLATE.format(query=req.prompt)
    logger.info({"prompt": prompt})
    req_data = {
        "model_name": req.model_name,
        "prompt": prompt,
        "history": req.history,
        "generation_configs": req.generation_configs,
        "stream": False
    }

    resp = requests.post(url=LLM_SERVER_PREFIX + LLM_SERVER_APIS['chat'],
                         json=req_data).json()

    if 'answer' in resp.keys():
        resp['time_cost'].update({'total': f"{time.time() - start:.3f}s"})
        retrieval = {}
        resp.update({'retrieval': retrieval})
        resp.update({'mermaid': parse_str_to_mermaid(resp['answer'])})

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
