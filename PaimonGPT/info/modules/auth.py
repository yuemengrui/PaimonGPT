# *_*coding:utf-8 *_*
# @Author : YueMengRui
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from configs import API_LIMIT, USERNAME_FILTER, TOKEN_EXPIRES
from info import logger, limiter, get_mysql_db
from fastapi.responses import JSONResponse
from .protocol import AuthRequest, AuthResponse, ErrorResponse
from info.utils.response_code import RET, error_map
from info.utils.crypto_context import crypto
from info.utils.Authentication import generate_token, verify_token
from info.mysql_models import User

router = APIRouter()


@router.api_route(path='/ai/auth/login', methods=['POST'], response_model=AuthResponse, summary="登录注册")
@limiter.limit(API_LIMIT['auth'])
def auth(request: Request,
         req: AuthRequest,
         mysql_db: Session = Depends(get_mysql_db)
         ):
    logger.info(str(req.dict()))

    if req.username.lower() in USERNAME_FILTER:
        return JSONResponse(ErrorResponse(errcode=RET.DATAERR, errmsg=u'非法用户名').dict(), status_code=500)

    user = mysql_db.query(User).filter(User.username == req.username).first()

    if user is None:
        new_user = User()
        new_user.username = req.username
        new_user.password = crypto.generate(req.password)
        try:
            mysql_db.add(new_user)  # 添加到会话
            mysql_db.commit()  # 提交到数据库
            mysql_db.flush()
            user_id = new_user.id
        except Exception as e:
            logger.error({'DB ERROR': e})
            mysql_db.rollback()
            return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

        token = generate_token(user_id)
        return AuthResponse(token=token, expires=TOKEN_EXPIRES)
    else:
        if not crypto.verify(req.password, user.password):
            return JSONResponse(ErrorResponse(errcode=RET.DATAERR, errmsg=u'密码错误').dict(), status_code=500)

    token = generate_token(user.id)
    return AuthResponse(token=token, expires=TOKEN_EXPIRES)


@router.api_route(path='/ai/auth/token/verify', methods=['GET'], summary="token verify")
@limiter.limit(API_LIMIT['auth'])
def auth(request: Request,
         user_id: int = Depends(verify_token)
         ):
    return JSONResponse({'state': 'success'})
