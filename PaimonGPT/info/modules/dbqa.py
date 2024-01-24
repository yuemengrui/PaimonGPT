# *_*coding:utf-8 *_*
# @Author : YueMengRui
import time
import json
import datetime
import requests
from fastapi import APIRouter, Request, Depends
from info.utils.Authentication import verify_token
from info import logger, limiter, DBs, LLM_Models
from configs import API_LIMIT, DBQA_PRESETS, LLM_SERVER_APIS
from configs.prompt_template import DBQA_PROMPT_TEMPLATE
from .protocol import DBConnectRequest, ErrorResponse, DBChatRequest, DBTableDataQueryRequest, DBDisconnectRequest
from fastapi.responses import JSONResponse, StreamingResponse
from info.utils.response_code import RET, error_map
from info.utils.api_servers.llm_base import servers_llm_chat
from info.utils.common import paser_str_to_json
from info.libs.DBQA.rdbms_db_summary import RdbmsSummary

router = APIRouter()


@router.api_route(path='/ai/dbqa/db/presets', methods=['GET'], summary="获取预设的DB列表")
@limiter.limit(API_LIMIT['base'])
def preset_db_list(request: Request,
                   user_id=Depends(verify_token)
                   ):
    return JSONResponse({'data': ['paimongpt']})


@router.api_route('/ai/dbqa/db/connect', methods=['POST'], summary="DB Connect")
@limiter.limit(API_LIMIT['base'])
def db_connect(request: Request,
               req: DBConnectRequest,
               user_id=Depends(verify_token)
               ):
    logger.info(str(req.dict()) + ' user_id: {}'.format(user_id))

    if req.preset and req.preset in DBQA_PRESETS.keys():
        db_name = req.preset
        kwargs = DBQA_PRESETS[req.preset]
    else:
        db_name = req.db_name
        kwargs = req.dict()

    try:
        db = RdbmsSummary(**kwargs)
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=u'数据库连接失败').dict(), status_code=500)
    else:
        table_info = db.get_table_info_with_json()
        DBs.update({db_name: db})

        return JSONResponse({'db_name': db_name, 'table_info': table_info})


@router.api_route('/ai/dbqa/db/disconnect', methods=['POST'], summary="DB disconnect")
@limiter.limit(API_LIMIT['base'])
def db_disconnect(request: Request,
                  req: DBDisconnectRequest,
                  user_id=Depends(verify_token)
                  ):
    logger.info(str(req.dict()) + ' user_id: {}'.format(user_id))

    try:
        DBs.pop(req.db_name)
    except Exception as e:
        logger.error({'EXCEPTION': e})

    return JSONResponse({'msg': 'success'})


@router.api_route('/ai/dbqa/db/table/data', methods=['POST'], summary="DB Table Data")
@limiter.limit(API_LIMIT['base'])
def get_db_table_data(request: Request,
                      req: DBTableDataQueryRequest,
                      user_id=Depends(verify_token)
                      ):
    logger.info(str(req.dict()) + ' user_id: {}'.format(user_id))

    sql = f"select * from {req.table_name} where id >= (select id from {req.table_name} order by id limit {int((req.page - 1) * req.page_size)}, 1) limit {req.page_size};"

    logger.info({'sql': sql})

    try:
        db_cls = DBs[req.db_name]
        db_res = db_cls.db.run(sql)
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    resp = []
    if len(db_res) > 1:
        resp.extend([dict(
            zip(db_res[0], [x.strftime('%Y-%m-%d %H:%M:%S') if isinstance(x, datetime.datetime) else x for x in i])) for
            i in db_res[1:]])

    return JSONResponse({'data': resp})


@router.api_route('/ai/dbqa/chat', methods=['POST'], summary="Chat")
@limiter.limit(API_LIMIT['chat'])
def dbqa_chat(request: Request,
              req: DBChatRequest,
              user_id=Depends(verify_token)
              ):
    logger.info(str(req.dict()) + ' user_id: {}'.format(user_id))
    start = time.time()

    def error_stream_generate(sql=''):
        res = {'answer': '抱歉，我不知道该问题的答案，请给我提供更多上下文我才能理解', 'time_cost': {}}
        res['time_cost'].update({'total': f"{time.time() - start:.3f}s"})
        res.update({'sql': sql, 'query_res': []})
        yield f"data: {json.dumps(res, ensure_ascii=False)}\n\n"

    try:
        db_cls = DBs[req.db_name]
        table_info = db_cls.get_related_table_summaries(req.prompt)
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return StreamingResponse(error_stream_generate(''), media_type="text/event-stream")

    prompt = DBQA_PROMPT_TEMPLATE.format(top_k=10, query=req.prompt, table_info=table_info)
    logger.info(f"prompt: {prompt}")

    resp = servers_llm_chat(prompt=prompt,
                            model_name=req.model_name,
                            history=req.history,
                            generation_configs=req.generation_configs)
    logger.info({'sql': resp})

    resp_json_data = paser_str_to_json(resp)
    logger.info({'sql': resp_json_data})

    sql = ''
    try:
        sql = resp_json_data['sql']
        if 'params' in resp_json_data:
            sql = sql % tuple(resp_json_data['params'])

        logger.info({'sql': sql})
        res = db_cls.db.run(sql)
        logger.info({'db res': res})
        results = []
        if len(res) > 1:
            results.extend(
                [dict(zip(res[0],
                          [x.strftime('%Y-%m-%d %H:%M:%S') if isinstance(x, datetime.datetime) else x for x in i]))
                 for i in res[1:]])

    except Exception as e:
        logger.error({'EXCEPTION': e})
        return StreamingResponse(error_stream_generate(sql), media_type="text/event-stream")
    else:
        if len(results) == 0:
            return StreamingResponse(error_stream_generate(sql), media_type="text/event-stream")
        else:
            prompt = f"你是一个出色的助手，我会给你用户的问题和mysql数据库的查询结果，你要根据数据库查询结果来回答用户的问题。\n用户的问题是：{req.prompt} \n数据库查询结果是：{str(results)}"
            req_data = {
                "model_name": req.model_name,
                "prompt": prompt,
                "history": req.history,
                "generation_configs": req.generation_configs,
                "stream": True
            }
            resp = requests.post(url=LLM_Models[req.model_name]['url_prefix'] + LLM_SERVER_APIS['chat'], json=req_data,
                                 stream=True)

            def stream_generate():
                for line in resp.iter_content(chunk_size=None):
                    res = json.loads(line.decode('utf-8'))
                    res['time_cost'].update({'total': f"{time.time() - start:.3f}s"})
                    res.update({'sql': sql, 'query_res': results})
                    yield f"data: {json.dumps(res, ensure_ascii=False)}\n\n"

            return StreamingResponse(stream_generate(), media_type="text/event-stream")
