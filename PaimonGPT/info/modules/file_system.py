# *_*coding:utf-8 *_*
# @Author : YueMengRui
import os
import time
from fastapi import APIRouter, Request, Depends, File, UploadFile
from sqlalchemy.orm import Session
from configs import API_LIMIT, FILE_SYSTEM_DIR, THIS_SERVER_URL
from info import logger, limiter, get_mysql_db
from fastapi.responses import JSONResponse, FileResponse
from info.utils.Authentication import verify_token
from info.mysql_models import FileSystem, UserFileSystem
from .protocol import ErrorResponse, FileUploadResponse
from info.utils.response_code import RET
from info.utils.get_md5 import md5hex
from configs import SECRET_KEY
import jwt

router = APIRouter()


@router.api_route(path='/ai/file/upload', methods=['POST'], response_model=FileUploadResponse, summary="文件上传")
@limiter.limit(API_LIMIT['auth'])
async def file_upload(request: Request,
                      file: UploadFile = File(...),
                      mysql_db: Session = Depends(get_mysql_db),
                      user_id: int = Depends(verify_token)
                      ):
    file_data = await file.read()

    file_ext = ''
    try:
        file_ext = '.' + file.filename.split('.')[-1]
    except Exception as e:
        logger.error({'EXCEPTION': e})

    file_hash = md5hex(file_data)

    if file_hash == '':
        return JSONResponse(ErrorResponse(errcode=RET.IOERR, errmsg=u'文件上传失败').dict(), status_code=500)

    file_system = mysql_db.query(FileSystem).filter(FileSystem.file_hash == file_hash).first()
    if file_system is None:
        file_dir = os.path.join(FILE_SYSTEM_DIR, file_hash[:2], file_hash[2:4])
        os.makedirs(file_dir, exist_ok=True)

        with open(os.path.join(file_dir, file_hash), 'wb') as f:
            f.write(file_data)

        time.sleep(0.02)

        with open(os.path.join(file_dir, file_hash), 'rb') as ff:
            if md5hex(ff.read()) != file_hash:
                return JSONResponse(ErrorResponse(errcode=RET.IOERR, errmsg=u'文件上传失败').dict(), status_code=500)

        new_file = FileSystem()
        new_file.file_hash = file_hash
        new_file.file_type = file.content_type
        new_file.file_size = file.size
        new_file.base_dir = FILE_SYSTEM_DIR
        new_file.file_ext = file_ext

        try:
            mysql_db.add(new_file)
            mysql_db.commit()
        except Exception as e:
            logger.error({'EXCEPTION': e})
            mysql_db.rollback()
            return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=u'文件上传失败').dict(), status_code=500)

    user_file = mysql_db.query(UserFileSystem).filter(UserFileSystem.file_hash == file_hash,
                                                      UserFileSystem.user_id == user_id).first()

    if user_file is None:
        new_user_file = UserFileSystem()
        new_user_file.file_hash = file_hash
        new_user_file.user_id = user_id
        new_user_file.file_name = file.filename
        mysql_db.add(new_user_file)
    else:
        user_file.file_name = file.filename

    try:
        mysql_db.commit()
    except Exception as e:
        logger.error({'EXCEPTION': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=u'文件上传失败').dict(), status_code=500)

    if file_ext:
        file_url = THIS_SERVER_URL + '/ai/file/' + file_hash + file_ext
    else:
        file_url = THIS_SERVER_URL + '/ai/file/' + file_hash

    return FileUploadResponse(file_hash=file_hash,
                              file_url=file_url,
                              file_name=file.filename,
                              file_size=file.size,
                              file_type=file.content_type,
                              file_ext=file_ext
                              )


@router.api_route(path='/ai/file/{file_path}', methods=['GET'])
@limiter.limit(API_LIMIT['auth'])
def file_download(request: Request,
                  file_path: str,
                  mysql_db: Session = Depends(get_mysql_db)
                  ):
    token = request.headers.get('Authorization')
    try:
        user_id = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])['user_id']
    except:
        user_id = None

    file_hash = file_path.split('.')[0]

    file = mysql_db.query(FileSystem).filter(FileSystem.file_hash == file_hash).first()
    if file is None:
        return JSONResponse(ErrorResponse(errcode=RET.NODATA, errmsg=u'文件不存在').dict(), status_code=500)

    file_path = os.path.join(file.base_dir, file_hash[:2], file_hash[2:4], file_hash)

    if not os.path.exists(file_path):
        return JSONResponse(ErrorResponse(errcode=RET.NODATA, errmsg=u'文件不存在').dict(), status_code=500)

    file_name = file_hash + file.file_ext
    if user_id:
        user_file = mysql_db.query(UserFileSystem).filter(UserFileSystem.file_hash == file_hash,
                                                          UserFileSystem.user_id == user_id).first()
        if user_file:
            if user_file.file_name:
                file_name = user_file.file_name

    return FileResponse(path=file_path, filename=file_name)


@router.api_route(path='/ai/file/upload/public', methods=['POST'], response_model=FileUploadResponse,
                  summary="文件上传公开版")
@limiter.limit(API_LIMIT['auth'])
async def file_upload_public(request: Request,
                             file: UploadFile = File(...),
                             mysql_db: Session = Depends(get_mysql_db)
                             ):
    file_data = await file.read()

    file_ext = ''
    try:
        file_ext = '.' + file.filename.split('.')[-1]
    except Exception as e:
        logger.error({'EXCEPTION': e})

    file_hash = md5hex(file_data)

    if file_hash == '':
        return JSONResponse(ErrorResponse(errcode=RET.IOERR, errmsg=u'文件上传失败').dict(), status_code=500)

    file_system = mysql_db.query(FileSystem).filter(FileSystem.file_hash == file_hash).first()
    if file_system is None:
        file_dir = os.path.join(FILE_SYSTEM_DIR, file_hash[:2], file_hash[2:4])
        os.makedirs(file_dir, exist_ok=True)

        with open(os.path.join(file_dir, file_hash), 'wb') as f:
            f.write(file_data)

        time.sleep(0.02)

        with open(os.path.join(file_dir, file_hash), 'rb') as ff:
            if md5hex(ff.read()) != file_hash:
                return JSONResponse(ErrorResponse(errcode=RET.IOERR, errmsg=u'文件上传失败').dict(), status_code=500)

        new_file = FileSystem()
        new_file.file_hash = file_hash
        new_file.file_type = file.content_type
        new_file.file_size = file.size
        new_file.base_dir = FILE_SYSTEM_DIR
        new_file.file_ext = file_ext

        try:
            mysql_db.add(new_file)
            mysql_db.commit()
        except Exception as e:
            logger.error({'EXCEPTION': e})
            mysql_db.rollback()
            return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=u'文件上传失败').dict(), status_code=500)

    if file_ext:
        file_url = THIS_SERVER_URL + '/ai/file/' + file_hash + file_ext
    else:
        file_url = THIS_SERVER_URL + '/ai/file/' + file_hash

    return FileUploadResponse(file_hash=file_hash,
                              file_url=file_url,
                              file_name=file.filename,
                              file_size=file.size,
                              file_type=file.content_type,
                              file_ext=file_ext
                              )
