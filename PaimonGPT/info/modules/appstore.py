# *_*coding:utf-8 *_*
# @Author : YueMengRui
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from configs import API_LIMIT
from info import logger, limiter, get_mysql_db
from fastapi.responses import JSONResponse
from info.utils.Authentication import verify_token
from info.mysql_models import SystemApp, App, ChatRecord, ChatMessageRecord, App_KB
from .protocol import AppCreateRequest, ErrorResponse, AppChatListRequest, AppChatCreateRequest, \
    AppChatMessageListRequest, AppDeleteRequest, AppCreateSystemAppRequest, AppInfoRequest, AppInfoModifyRequest, \
    AppChatDeleteRequest
from info.utils.response_code import RET, error_map

router = APIRouter()


@router.api_route(path='/ai/system_app/list', methods=['GET'], summary="system app list")
@limiter.limit(API_LIMIT['auth'])
def get_system_app_list(request: Request,
                        mysql_db: Session = Depends(get_mysql_db),
                        user_id: int = Depends(verify_token)
                        ):
    system_app_list = mysql_db.query(SystemApp).filter(SystemApp.is_delete == False).order_by(
        SystemApp.update_time.desc()).all()

    return JSONResponse({'list': [x.to_dict() for x in system_app_list]})


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
        temp['kbs'] = []
        app_kb = mysql_db.query(App_KB).filter(App_KB.app_id == app.id).all()
        if app_kb:
            temp['kbs'] = [{'kb_id': x.kb_id, 'kb_name': x.kb_name} for x in app_kb]

        res.append(temp)

    return JSONResponse({'list': res})


@router.api_route(path='/ai/app/info', methods=['POST'], summary="app info")
@limiter.limit(API_LIMIT['auth'])
def get_app_info(request: Request,
                 req: AppInfoRequest,
                 mysql_db: Session = Depends(get_mysql_db),
                 user_id: int = Depends(verify_token)
                 ):
    app_info = mysql_db.query(App).filter(App.id == req.app_id, App.is_delete == False).first()

    if app_info is None:
        return JSONResponse(ErrorResponse(errcode=RET.NODATA, errmsg=error_map[RET.NODATA]).dict(), status_code=400)

    resp = app_info.to_dict()
    resp['kbs'] = []
    app_kb = mysql_db.query(App_KB).filter(App_KB.app_id == app_info.id).all()
    if app_kb:
        resp['kbs'] = [{'kb_id': x.kb_id, 'kb_name': x.kb_name} for x in app_kb]

    return JSONResponse(resp)


@router.api_route(path='/ai/app/info/modify', methods=['POST'], summary="app info modify")
@limiter.limit(API_LIMIT['auth'])
def app_info_modify(request: Request,
                    req: AppInfoModifyRequest,
                    mysql_db: Session = Depends(get_mysql_db),
                    user_id: int = Depends(verify_token)
                    ):
    app_info = mysql_db.query(App).filter(App.id == req.app_id, App.is_delete == False).first()

    if app_info is None:
        return JSONResponse(ErrorResponse(errcode=RET.NODATA, errmsg=error_map[RET.NODATA]).dict(), status_code=400)

    if app_info.is_system:
        app_info.llm_name = req.llm_name
    else:
        app_info.name = req.name
        app_info.llm_name = req.llm_name

    if len(req.kbs) > 0:
        mysql_db.query(App_KB).filter(App_KB.app_id == req.app_id).delete()

        for kb in req.kbs:
            app_kb = App_KB()
            app_kb.app_id = req.app_id
            app_kb.kb_id = kb['kb_id']
            app_kb.kb_name = kb['kb_name']
            mysql_db.add(app_kb)

    try:
        mysql_db.commit()
    except Exception as e:
        logger.error({'DB ERROR': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    return JSONResponse({'msg': error_map[RET.OK]})


@router.api_route(path='/ai/app/create/system_app/list', methods=['GET'], summary="app list")
@limiter.limit(API_LIMIT['auth'])
def get_app_create_user_system_app_list(request: Request,
                                        mysql_db: Session = Depends(get_mysql_db),
                                        user_id: int = Depends(verify_token)
                                        ):
    system_app_list = mysql_db.query(SystemApp).filter(SystemApp.is_delete == False).all()

    if len(system_app_list) == 0:
        return JSONResponse({'list': []})

    user_system_app_list = mysql_db.query(App).filter(App.user_id == user_id, App.is_system == True,
                                                      App.is_delete == False).all()

    user_system_app_id_list = [x.system_app_id for x in user_system_app_list]

    res = []
    for sys_app in system_app_list:
        if sys_app.id not in user_system_app_id_list:
            res.append(sys_app.to_dict())

    return JSONResponse({'list': res})


@router.api_route(path='/ai/app/create/system_app', methods=['POST'], summary="app create")
@limiter.limit(API_LIMIT['auth'])
def user_system_app_create(request: Request,
                           req: AppCreateSystemAppRequest,
                           mysql_db: Session = Depends(get_mysql_db),
                           user_id: int = Depends(verify_token)
                           ):
    app = mysql_db.query(App).filter(App.user_id == user_id, App.is_system == True,
                                     App.system_app_id == req.system_app_id).first()
    if app is not None:
        app.is_delete = False
    else:
        sys_app = mysql_db.query(SystemApp).get(req.system_app_id)
        if sys_app is None:
            return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

        new_app = App()
        new_app.user_id = user_id
        new_app.name = sys_app.name
        if sys_app.name == '图文理解':
            new_app.llm_name = 'Qwen_VL'
        else:
            new_app.llm_name = 'Baichuan2_13B_8k'
        new_app.is_system = True
        new_app.system_app_id = req.system_app_id
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
    new_app.user_id = user_id
    new_app.name = req.name
    new_app.llm_name = req.llm_name
    mysql_db.add(new_app)
    mysql_db.flush()

    if len(req.kbs) > 0:
        for kb in req.kbs:
            app_kb = App_KB()
            app_kb.app_id = new_app.id
            app_kb.kb_id = kb['kb_id']
            app_kb.kb_name = kb['kb_name']
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
