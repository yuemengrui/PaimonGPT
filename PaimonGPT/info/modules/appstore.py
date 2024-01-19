# *_*coding:utf-8 *_*
# @Author : YueMengRui
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from configs import API_LIMIT
from info import logger, limiter, get_mysql_db
from fastapi.responses import JSONResponse
from info.utils.Authentication import verify_token
from info.mysql_models import AppStore
from .protocol import ErrorResponse, AppStoreAppInstallRequest, AppStoreAppUninstallRequest
from info.utils.response_code import RET, error_map
from info.utils.UniqueID import snowflake

router = APIRouter()


@router.api_route(path='/ai/appstore/app/list', methods=['GET'], summary="appstore app list")
@limiter.limit(API_LIMIT['base'])
def get_appstore_app_list(request: Request,
                          mysql_db: Session = Depends(get_mysql_db),
                          user_id: int = Depends(verify_token)
                          ):
    store_app_list = mysql_db.query(AppStore).filter(AppStore.is_installed == True).order_by(
        AppStore.update_time.desc()).all()

    return JSONResponse({'data': [x.to_dict() for x in store_app_list]})


@router.api_route(path='/ai/appstore/app/install', methods=['POST'], summary="上架APP到商城")
@limiter.limit(API_LIMIT['base'])
def appstore_app_install(request: Request,
                         req: AppStoreAppInstallRequest,
                         mysql_db: Session = Depends(get_mysql_db),
                         user_id: int = Depends(verify_token)
                         ):
    logger.info(req.dict())

    new_app = AppStore()
    new_app.uid = snowflake.guid()
    new_app.name = req.name
    new_app.module_name = req.module_name
    new_app.description = req.description

    try:
        mysql_db.add(new_app)
        mysql_db.commit()
    except Exception as e:
        logger.error({'DB ERROR': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    return JSONResponse({'msg': error_map[RET.OK]})


@router.api_route(path='/ai/appstore/app/uninstall', methods=['POST'], summary="从商城下架APP")
@limiter.limit(API_LIMIT['base'])
def appstore_app_uninstall(request: Request,
                           req: AppStoreAppUninstallRequest,
                           mysql_db: Session = Depends(get_mysql_db),
                           user_id: int = Depends(verify_token)
                           ):
    logger.info(req.dict())

    mysql_db.query(AppStore).filter(AppStore.uid == req.app_id).update({'is_installed': False})
    try:
        mysql_db.commit()
    except Exception as e:
        logger.error({'DB ERROR': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    return JSONResponse({'msg': error_map[RET.OK]})
