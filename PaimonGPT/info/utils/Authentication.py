# *_*coding:utf-8 *_*
import datetime
from fastapi import Request, HTTPException
from mylogger import logger
from configs import SECRET_KEY, TOKEN_EXPIRES
import jwt


def generate_token(user_id):
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=TOKEN_EXPIRES),
        "user_id": user_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token


def verify_token(request: Request):
    token = request.headers.get('Authorization')
    try:
        user_id = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])['user_id']
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail=u'token已过期',
                            headers={"Content-Type": "application/json;charset=UTF-8"})
    except Exception as e:
        logger.error({'EXCEPTION': e})
        raise HTTPException(status_code=401, detail=u'非法请求',
                            headers={"Content-Type": "application/json;charset=UTF-8"})
