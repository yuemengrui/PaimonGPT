# *_*coding:utf-8 *_*
# @Author : YueMengRui
from fastapi import APIRouter, Request
from configs import API_LIMIT
from info import limiter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.api_route(path='/ai/health', methods=['GET'], summary="health")
@limiter.limit(API_LIMIT['base'])
async def health(request: Request):
    return JSONResponse({'msg': 'I am very healthy'})
