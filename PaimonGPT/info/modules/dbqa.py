# *_*coding:utf-8 *_*
# @Author : YueMengRui
import datetime
from fastapi import APIRouter, Request, Depends
from info.utils.Authentication import verify_token
from info import logger, limiter, DBs
from configs import API_LIMIT, DBQA_PRESETS
from configs.prompt_template import DBQA_PROMPT_TEMPLATE
from .protocol import DBConnectRequest, ErrorResponse, DBChatRequest, DBTableDataQueryRequest, DBDisconnectRequest
from fastapi.responses import JSONResponse
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

    try:
        db_cls = DBs[req.db_name]
        table_info = db_cls.db.table_info
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    prompt = DBQA_PROMPT_TEMPLATE.format(top_k=10, query=req.prompt, table_info=table_info)
    logger.info(f"prompt: {prompt}")

    resp = servers_llm_chat(prompt=prompt,
                            model_name=req.model_name,
                            history=req.history,
                            generation_configs=req.generation_configs)
    logger.info({'sql': resp})

    resp_json_data = paser_str_to_json(resp)
    logger.info({'sql': resp_json_data})

    try:
        sql = resp_json_data['sql']
        if 'params' in resp_json_data:
            sql = sql % tuple(resp_json_data['params'])

        logger.info({'sql': sql})
        res = db_cls.db.run(sql)
        return JSONResponse({'data': res})
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return JSONResponse(ErrorResponse(errcode=RET.SERVERERR, errmsg=error_map[RET.SERVERERR]).dict(),
                            status_code=500)
