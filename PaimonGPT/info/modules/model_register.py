# *_*coding:utf-8 *_*
# @Author : YueMengRui
from fastapi import APIRouter, Request
from configs import API_LIMIT
from info import logger, limiter, LLM_Models, Embedding_Models
from fastapi.responses import JSONResponse
from info.utils.response_code import RET, error_map
from .protocol import ErrorResponse, ModelRegisterRequest

router = APIRouter()


@router.api_route(path='/ai/model/register', methods=['POST'], summary="model register")
@limiter.limit(API_LIMIT['text_embedding'])
def model_register(request: Request,
                   req: ModelRegisterRequest
                   ):
    logger.info(str(req.dict()))

    if req.type == 'llm':
        if req.model_name in LLM_Models:
            return JSONResponse(ErrorResponse(errcode=RET.DATAERR, errmsg='已存在同名模型').dict(), status_code=500)

        LLM_Models.update({req.model_name: {'url_prefix': req.url_prefix, 'info': req.info}})
    elif req.type == 'embedding':
        if req.model_name in Embedding_Models:
            return JSONResponse(ErrorResponse(errcode=RET.DATAERR, errmsg='已存在同名模型').dict(), status_code=500)

        Embedding_Models.update({req.model_name: {'url_prefix': req.url_prefix, 'info': req.info}})

    return JSONResponse({'msg': u'成功'})
