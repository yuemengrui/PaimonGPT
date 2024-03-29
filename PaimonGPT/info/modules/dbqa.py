# *_*coding:utf-8 *_*
# @Author : YueMengRui
import time
import json
import datetime
import requests
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends
from info.utils.Authentication import verify_token
from info import logger, limiter, DBs, Embedding_Models, get_mysql_db
from configs import API_LIMIT, DBQA_PRESETS, LLM_SERVER_APIS, LLM_SERVER_PREFIX
from configs.prompt_template import DBQA_PROMPT_TEMPLATE
from .protocol import DBConnectRequest, ErrorResponse, DBChatRequest, DBTableDataQueryRequest, DBDisconnectRequest, \
    DBTableDescriptionRequest
from fastapi.responses import JSONResponse, StreamingResponse
from info.utils.response_code import RET, error_map
from info.utils.api_servers.llm_base import servers_llm_chat
from info.utils.common import paser_str_to_json
from info.libs.DBQA.rdbms_db_summary import RdbmsSummary
from info.mysql_models import DBQADB, DBQADBTableDescription, ChatRecord, ChatMessageRecord

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
               mysql_db: Session = Depends(get_mysql_db),
               user_id=Depends(verify_token)
               ):
    logger.info(str(req.dict()) + ' user_id: {}'.format(user_id))

    if req.preset and req.preset in DBQA_PRESETS.keys():
        host = DBQA_PRESETS[req.preset]['host']
        port = DBQA_PRESETS[req.preset]['port']
        username = DBQA_PRESETS[req.preset]['username']
        password = DBQA_PRESETS[req.preset]['password']
        db_name = DBQA_PRESETS[req.preset]['db_name']
    else:
        host = req.host
        port = req.port
        username = req.username
        password = req.password
        db_name = req.db_name

    embedding_model = list(Embedding_Models.keys())[0] if len(Embedding_Models) > 0 else None

    try:
        db = RdbmsSummary(host=host, port=port, username=username, password=password, db_name=db_name,
                          embedding_model=embedding_model)
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=u'数据库连接失败').dict(), status_code=500)
    else:
        table_description = []
        origin_table_info = db.get_table_info_all()

        dbqa_db = mysql_db.query(DBQADB).filter(DBQADB.user_id == user_id,
                                                DBQADB.host == host,
                                                DBQADB.port == port,
                                                DBQADB.username == username,
                                                DBQADB.db_name == db_name).first()
        if dbqa_db:
            chat_id = dbqa_db.chat_id
            for table_name in db.tables:
                table_desc = mysql_db.query(DBQADBTableDescription).filter(
                    DBQADBTableDescription.db_id == dbqa_db.id, DBQADBTableDescription.table_name == table_name).first()
                if table_desc:
                    table_description.append({
                        'table_name': table_name,
                        'table_comment': table_desc.table_comment,
                        'is_deprecated': table_desc.is_deprecated,
                        'columns': table_desc.columns,
                        'examples': table_desc.examples if table_desc.examples else []
                    })
                else:
                    table_comment, columns = db.get_table_info_by_table(table_name)
                    table_description.append({
                        'table_name': table_name,
                        'table_comment': table_comment,
                        'is_deprecated': False,
                        'columns': columns,
                        'examples': []
                    })
        else:
            for table_name in db.tables:
                table_comment, columns = db.get_table_info_by_table(table_name)
                table_description.append({
                    'table_name': table_name,
                    'table_comment': table_comment,
                    'is_deprecated': False,
                    'columns': columns,
                    'examples': []
                })
            new_chat = ChatRecord()
            new_chat.app_id = req.app_id
            mysql_db.add(new_chat)
            mysql_db.flush()
            chat_id = new_chat.id

            new_db = DBQADB()
            new_db.user_id = user_id
            new_db.chat_id = chat_id
            new_db.host = host
            new_db.port = port
            new_db.username = username
            new_db.db_name = db_name
            mysql_db.add(new_db)

            try:
                mysql_db.commit()
            except Exception as e:
                logger.error({'DB ERROR': e})
                mysql_db.rollback()
                return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(),
                                    status_code=500)

        db.load_table_embeddings(table_description)
        DBs.update({db_name: db})

        return JSONResponse(
            {'db_name': db_name, 'chat_id': chat_id, 'origin_table_info': origin_table_info,
             'table_description': table_description})


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


@router.api_route('/ai/dbqa/db/table/description', methods=['POST'], summary="DB Table Description")
@limiter.limit(API_LIMIT['base'])
def db_table_description(request: Request,
                         req: DBTableDescriptionRequest,
                         mysql_db: Session = Depends(get_mysql_db),
                         user_id=Depends(verify_token)
                         ):
    logger.info(str(req.dict()) + ' user_id: {}'.format(user_id))

    dbqa_db = mysql_db.query(DBQADB).filter(DBQADB.user_id == user_id, DBQADB.db_name == req.db_name).first()

    if dbqa_db is None:
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(),
                            status_code=500)

    for t in req.table_description:
        t_desc = mysql_db.query(DBQADBTableDescription).filter(DBQADBTableDescription.db_id == dbqa_db.id,
                                                               DBQADBTableDescription.table_name == t[
                                                                   'table_name']).first()
        if t_desc:
            t_desc.table_comment = t.get('table_comment')
            t_desc.columns = t.get('columns')
            t_desc.is_deprecated = t.get('is_deprecated')
            t_desc.examples = t.get('examples')
        else:
            table_desc = DBQADBTableDescription()
            table_desc.db_id = dbqa_db.id
            table_desc.table_name = t['table_name']
            table_desc.table_comment = t.get('table_comment')
            table_desc.columns = t.get('columns')
            table_desc.is_deprecated = t.get('is_deprecated')
            table_desc.examples = t.get('examples')
            mysql_db.add(table_desc)

    try:
        mysql_db.commit()
    except Exception as e:
        logger.error({'DB ERROR': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(),
                            status_code=500)

    try:
        db_cls = DBs[req.db_name]
        db_cls.load_table_embeddings(req.table_description)
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(),
                            status_code=500)
    return JSONResponse({'msg': '成功'})


@router.api_route('/ai/dbqa/db/table/data', methods=['POST'], summary="DB Table Data")
@limiter.limit(API_LIMIT['base'])
def get_db_table_data(request: Request,
                      req: DBTableDataQueryRequest,
                      user_id=Depends(verify_token)
                      ):
    logger.info(str(req.dict()) + ' user_id: {}'.format(user_id))

    # sql = f"select * from {req.table_name} where id >= (select id from {req.table_name} order by id limit {int((req.page - 1) * req.page_size)}, 1) limit {req.page_size};"
    sql = f"select * from {req.table_name} limit {int((req.page - 1) * req.page_size)}, {req.page_size};"

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
            zip(db_res[0],
                [x.strftime('%Y-%m-%d %H:%M:%S') if isinstance(x, (datetime.datetime, datetime.date)) else x for x in
                 i])) for
            i in db_res[1:]])

    return JSONResponse({'data': resp})


@router.api_route('/ai/dbqa/chat', methods=['POST'], summary="Chat")
@limiter.limit(API_LIMIT['chat'])
def dbqa_chat(request: Request,
              req: DBChatRequest,
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

    def error_stream_generate(sql=''):
        res = {'answer': '抱歉，我不知道该问题的答案，请给我提供更多上下文我才能理解', 'time_cost': {}}
        res['time_cost'].update({'total': f"{time.time() - start:.3f}s"})
        res.update({'sql': sql, 'query_res': []})
        yield f"data: {json.dumps(res, ensure_ascii=False)}\n\n"

        new_message_assistant = ChatMessageRecord()
        new_message_assistant.chat_id = req.chat_id
        new_message_assistant.uid = req.answer_uid
        new_message_assistant.role = 'assistant'
        new_message_assistant.content = res['answer']
        new_message_assistant.llm_name = req.model_name
        new_message_assistant.response = res
        mysql_db.add(new_message_assistant)
        try:
            mysql_db.commit()
        except Exception as e:
            logger.error({'DB ERROR': e})
            mysql_db.rollback()

    try:
        db_cls = DBs[req.db_name]
        table_info, table_examples = db_cls.get_related_table_summaries(req.prompt, req.limit, req.threshold)
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return StreamingResponse(error_stream_generate(''), media_type="text/event-stream")

    prompt = DBQA_PROMPT_TEMPLATE.format(top_k=10, examples=table_examples, query=req.prompt, table_info=table_info)
    logger.info({"prompt": prompt})

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
            resp = requests.post(url=LLM_SERVER_PREFIX + LLM_SERVER_APIS['chat'], json=req_data,
                                 stream=True)

            def stream_generate():
                for line in resp.iter_content(chunk_size=None):
                    res = json.loads(line.decode('utf-8'))
                    res['time_cost'].update({'total': f"{time.time() - start:.3f}s"})
                    res.update({'sql': sql, 'query_res': results})
                    yield f"data: {json.dumps(res, ensure_ascii=False)}\n\n"

                new_message_assistant = ChatMessageRecord()
                new_message_assistant.chat_id = req.chat_id
                new_message_assistant.uid = req.answer_uid
                new_message_assistant.role = 'assistant'
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
