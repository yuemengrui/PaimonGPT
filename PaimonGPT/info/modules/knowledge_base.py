# *_*coding:utf-8 *_*
# @Author : YueMengRui
from fastapi import APIRouter, Request, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from configs import API_LIMIT
from info import logger, limiter, get_mysql_db
from fastapi.responses import JSONResponse
from info.utils.Authentication import verify_token
from info.mysql_models import KB, KBFile, KBFileChunks
from .protocol import ErrorResponse, KBCreateRequest, KBDataImportRequest, KBDeleteRequest, KBDataListRequest, \
    KBDataDetailRequest, KBDataDeleteRequest
from info.utils.response_code import RET, error_map
from info.background_tasks.kb_import_data import import_data_2_kb
from info.utils.UniqueID import snowflake

router = APIRouter()


@router.api_route(path='/ai/kb/list', methods=['GET'], summary="knowledge base list")
@limiter.limit(API_LIMIT['auth'])
def get_kb_list(request: Request,
                mysql_db: Session = Depends(get_mysql_db),
                user_id: int = Depends(verify_token)
                ):
    kb_list = mysql_db.query(KB).filter(KB.user_id == user_id, KB.is_delete == False).order_by(
        KB.update_time.desc()).all()

    return JSONResponse({'list': [x.to_dict() for x in kb_list]})


@router.api_route(path='/ai/kb/create', methods=['POST'], summary="knowledge_base create")
@limiter.limit(API_LIMIT['auth'])
def kb_create(request: Request,
              req: KBCreateRequest,
              mysql_db: Session = Depends(get_mysql_db),
              user_id: int = Depends(verify_token)
              ):
    logger.info(str(req.dict()))
    new_kb = KB()
    new_kb.uid = snowflake.guid()
    new_kb.user_id = user_id
    new_kb.name = req.name
    new_kb.description = req.description
    new_kb.embedding_model = req.embedding_model

    try:
        mysql_db.add(new_kb)
        mysql_db.commit()
    except Exception as e:
        logger.error({'DB ERROR': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    return JSONResponse({'msg': error_map[RET.OK]})


@router.api_route(path='/ai/kb/delete', methods=['POST'], summary="knowledge_base create")
@limiter.limit(API_LIMIT['auth'])
def kb_delete(request: Request,
              req: KBDeleteRequest,
              mysql_db: Session = Depends(get_mysql_db),
              user_id: int = Depends(verify_token)
              ):
    logger.info(str(req.dict()) + ' user_id: ' + str(user_id))

    mysql_db.query(KB).filter(KB.uid == req.kb_id, KB.user_id == user_id).update({'is_delete': True})
    try:
        mysql_db.commit()
    except Exception as e:
        logger.error({'DB ERROR': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    return JSONResponse({'msg': error_map[RET.OK]})


@router.api_route(path='/ai/kb/file/list', methods=['POST'], summary="knowledge_base file list")
@limiter.limit(API_LIMIT['auth'])
def kb_data_list(request: Request,
                 req: KBDataListRequest,
                 mysql_db: Session = Depends(get_mysql_db),
                 user_id: int = Depends(verify_token)
                 ):
    logger.info(str(req.dict()) + ' user_id: ' + str(user_id))

    file_list = mysql_db.query(KBFile).filter(KBFile.kb_id == req.kb_id, KBFile.is_delete == False).order_by(
        KBFile.create_time.desc()).all()

    return JSONResponse({'list': [x.to_dict() for x in file_list]})


@router.api_route(path='/ai/kb/file/import', methods=['POST'], summary="knowledge_base import file")
@limiter.limit(API_LIMIT['auth'])
def kb_data_import(request: Request,
                   req: KBDataImportRequest,
                   background_tasks: BackgroundTasks,
                   mysql_db: Session = Depends(get_mysql_db),
                   user_id: int = Depends(verify_token)
                   ):
    logger.info(str(req.dict()))

    background_tasks.add_task(import_data_2_kb, req, mysql_db)

    return JSONResponse({'msg': error_map[RET.OK]})


@router.api_route(path='/ai/kb/file/chunks', methods=['POST'], summary="knowledge_base file chunks")
@limiter.limit(API_LIMIT['auth'])
def kb_data_detail(request: Request,
                   req: KBDataDetailRequest,
                   mysql_db: Session = Depends(get_mysql_db),
                   user_id: int = Depends(verify_token)
                   ):
    logger.info(str(req.dict()) + ' user_id: ' + str(user_id))

    chunk_list = mysql_db.query(KBFileChunks).filter(KBFileChunks.file_id == req.file_id).all()

    return JSONResponse({'list': [x.to_dict() for x in chunk_list]})


@router.api_route(path='/ai/kb/file/delete', methods=['POST'], summary="knowledge_base file delete")
@limiter.limit(API_LIMIT['auth'])
def kb_data_delete(request: Request,
                   req: KBDataDeleteRequest,
                   mysql_db: Session = Depends(get_mysql_db),
                   user_id: int = Depends(verify_token)
                   ):
    logger.info(str(req.dict()) + ' user_id: ' + str(user_id))

    mysql_db.query(KBFile).filter(KBFile.id == req.data_id).update({'is_delete': True})
    try:
        mysql_db.commit()
    except Exception as e:
        logger.error({'DB ERROR': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    return JSONResponse({'msg': error_map[RET.OK]})
