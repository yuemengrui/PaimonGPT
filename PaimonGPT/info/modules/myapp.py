# *_*coding:utf-8 *_*
# @Author : YueMengRui
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from configs import API_LIMIT
from info import logger, limiter, get_mysql_db, LLM_Models
from fastapi.responses import JSONResponse
from info.utils.Authentication import verify_token
from info.mysql_models import App, AppStore, ChatRecord, ChatMessageRecord, App_KB
from .protocol import AppCreateRequest, ErrorResponse, AppChatListRequest, AppChatCreateRequest, \
    AppChatMessageListRequest, AppDeleteRequest, AppInfoRequest, AppInfoModifyRequest, AppChatDeleteRequest, \
    AppCreateFromAppStoreRequest
from info.utils.response_code import RET, error_map
from info.utils.UniqueID import snowflake

router = APIRouter()


@router.api_route(path='/ai/app/list', methods=['GET'], summary="app list")
@limiter.limit(API_LIMIT['auth'])
def get_app_list(request: Request,
                 mysql_db: Session = Depends(get_mysql_db),
                 user_id: int = Depends(verify_token)
                 ):
    app_list = mysql_db.query(App).filter(App.user_id == user_id, App.is_delete == False).order_by(
        App.update_time.desc()).all()

    res = []
    for app in app_list:
        temp = app.to_dict()

        if app.is_appstore:
            store_app = mysql_db.query(AppStore).filter(AppStore.uid == app.appstore_uid).first()
            temp.update({'module_name': store_app.module_name, 'is_installed': store_app.is_installed})

        temp['kbs'] = []
        app_kb = mysql_db.query(App_KB).filter(App_KB.app_id == app.uid).all()
        if app_kb:
            temp['kbs'] = [{'id': x.kb_id, 'name': x.kb_name} for x in app_kb]

        res.append(temp)

    return JSONResponse({'list': res})


@router.api_route(path='/ai/app/info', methods=['POST'], summary="app info")
@limiter.limit(API_LIMIT['auth'])
def get_app_info(request: Request,
                 req: AppInfoRequest,
                 mysql_db: Session = Depends(get_mysql_db),
                 user_id: int = Depends(verify_token)
                 ):
    app_info = mysql_db.query(App).filter(App.uid == req.app_id, App.is_delete == False).first()

    if app_info is None:
        return JSONResponse(ErrorResponse(errcode=RET.NODATA, errmsg=error_map[RET.NODATA]).dict(), status_code=400)

    resp = app_info.to_dict()
    if app_info.is_appstore:
        store_app = mysql_db.query(AppStore).filter(AppStore.uid == app_info.appstore_uid).first()
        resp.update({'module_name': store_app.module_name, 'is_installed': store_app.is_installed})

    resp['kbs'] = []
    app_kb = mysql_db.query(App_KB).filter(App_KB.app_id == app_info.uid).all()
    if app_kb:
        resp['kbs'] = [{'id': x.kb_id, 'name': x.kb_name} for x in app_kb]

    return JSONResponse(resp)


@router.api_route(path='/ai/app/info/modify', methods=['POST'], summary="app info modify")
@limiter.limit(API_LIMIT['auth'])
def app_info_modify(request: Request,
                    req: AppInfoModifyRequest,
                    mysql_db: Session = Depends(get_mysql_db),
                    user_id: int = Depends(verify_token)
                    ):
    app_info = mysql_db.query(App).filter(App.uid == req.app_id, App.is_delete == False).first()

    if app_info is None:
        return JSONResponse(ErrorResponse(errcode=RET.NODATA, errmsg=error_map[RET.NODATA]).dict(), status_code=400)

    app_info.name = req.name
    app_info.llm_name = req.llm_name
    app_info.description = req.description

    if len(req.kbs) > 0:
        mysql_db.query(App_KB).filter(App_KB.app_id == req.app_id).delete()

        for kb in req.kbs:
            app_kb = App_KB()
            app_kb.app_id = req.app_id
            app_kb.kb_id = kb['id']
            app_kb.kb_name = kb['name']
            mysql_db.add(app_kb)

    try:
        mysql_db.commit()
    except Exception as e:
        logger.error({'DB ERROR': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    return JSONResponse({'msg': error_map[RET.OK]})


@router.api_route(path='/ai/app/create/from_appstore', methods=['POST'], summary="app create from appstore")
@limiter.limit(API_LIMIT['base'])
def app_create(request: Request,
               req: AppCreateFromAppStoreRequest,
               mysql_db: Session = Depends(get_mysql_db),
               user_id: int = Depends(verify_token)
               ):
    store_app = mysql_db.query(AppStore).filter(AppStore.uid == req.app_id).first()
    if not store_app:
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    new_app = App()
    new_app.uid = snowflake.guid()
    new_app.user_id = user_id
    new_app.name = store_app.name
    new_app.llm_name = list(LLM_Models.keys())[0] if len(list(LLM_Models.keys())) > 0 else ''
    new_app.description = store_app.description
    new_app.is_appstore = True
    new_app.appstore_uid = req.app_id
    mysql_db.add(new_app)

    try:
        mysql_db.commit()
    except Exception as e:
        logger.error({'DB ERROR': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    return JSONResponse({'msg': error_map[RET.OK]})


@router.api_route(path='/ai/app/create', methods=['POST'], summary="app create")
@limiter.limit(API_LIMIT['auth'])
def app_create(request: Request,
               req: AppCreateRequest,
               mysql_db: Session = Depends(get_mysql_db),
               user_id: int = Depends(verify_token)
               ):
    new_app = App()
    new_app.uid = snowflake.guid()
    new_app.user_id = user_id
    new_app.name = req.name
    new_app.llm_name = req.llm_name
    mysql_db.add(new_app)
    mysql_db.flush()

    if len(req.kbs) > 0:
        for kb in req.kbs:
            app_kb = App_KB()
            app_kb.app_id = new_app.id
            app_kb.kb_id = kb['id']
            app_kb.kb_name = kb['name']
            mysql_db.add(app_kb)

    try:
        mysql_db.commit()
    except Exception as e:
        logger.error({'DB ERROR': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    return JSONResponse({'msg': error_map[RET.OK]})


@router.api_route(path='/ai/app/delete', methods=['POST'], summary="app delete")
@limiter.limit(API_LIMIT['auth'])
def app_delete(request: Request,
               req: AppDeleteRequest,
               mysql_db: Session = Depends(get_mysql_db),
               user_id: int = Depends(verify_token)
               ):
    logger.info(str(req.dict()) + ' user_id: ' + str(user_id))

    mysql_db.query(App).filter(App.id == req.app_id, App.user_id == user_id).update({'is_delete': True})

    try:
        mysql_db.commit()
    except Exception as e:
        logger.error({'DB ERROR': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    return JSONResponse({'msg': error_map[RET.OK]})


@router.api_route(path='/ai/app/chat/list', methods=['POST'], summary="app chat list")
@limiter.limit(API_LIMIT['auth'])
def app_chat_list(request: Request,
                  req: AppChatListRequest,
                  mysql_db: Session = Depends(get_mysql_db),
                  user_id: int = Depends(verify_token)
                  ):
    chat_list = mysql_db.query(ChatRecord).filter(ChatRecord.app_id == req.app_id,
                                                  ChatRecord.is_delete == False).order_by(
        ChatRecord.update_time.desc()).all()

    return JSONResponse({'list': [x.to_dict() for x in chat_list]})


@router.api_route(path='/ai/app/chat/create', methods=['POST'], summary="app chat list")
@limiter.limit(API_LIMIT['auth'])
def app_chat_create(request: Request,
                    req: AppChatCreateRequest,
                    mysql_db: Session = Depends(get_mysql_db),
                    user_id: int = Depends(verify_token)
                    ):
    new_chat = ChatRecord()
    new_chat.app_id = req.app_id
    new_chat.name = req.name

    try:
        mysql_db.add(new_chat)
        mysql_db.commit()
    except Exception as e:
        logger.error({'DB ERROR': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    return JSONResponse({'msg': error_map[RET.OK]})


@router.api_route(path='/ai/app/chat/delete', methods=['POST'], summary="app chat delete")
@limiter.limit(API_LIMIT['auth'])
def app_chat_create(request: Request,
                    req: AppChatDeleteRequest,
                    mysql_db: Session = Depends(get_mysql_db),
                    user_id: int = Depends(verify_token)
                    ):
    logger.info(str(req.dict()) + ' user_id: ' + str(user_id))

    mysql_db.query(ChatRecord).filter(ChatRecord.id == req.chat_id).update({'is_delete': True})

    try:
        mysql_db.commit()
    except Exception as e:
        logger.error({'DB ERROR': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    return JSONResponse({'msg': error_map[RET.OK]})


@router.api_route(path='/ai/app/chat/message/list', methods=['POST'], summary="app chat message list")
@limiter.limit(API_LIMIT['auth'])
def app_chat_message_list(request: Request,
                          req: AppChatMessageListRequest,
                          mysql_db: Session = Depends(get_mysql_db),
                          user_id: int = Depends(verify_token)
                          ):
    message_list = mysql_db.query(ChatMessageRecord).filter(ChatMessageRecord.chat_id == req.chat_id,
                                                            ChatMessageRecord.is_delete == False).order_by(
        ChatMessageRecord.id.desc()).offset((req.page_size * (req.page - 1))).limit(req.page_size)

    return JSONResponse({'list': [x.to_dict() for x in message_list[::-1]]})
