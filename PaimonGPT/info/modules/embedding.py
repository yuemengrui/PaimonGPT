# *_*coding:utf-8 *_*
# @Author : YueMengRui
from fastapi import APIRouter, Request, Depends
from configs import API_LIMIT
from info import logger, limiter, Embedding_Models
from fastapi.responses import JSONResponse
from .protocol import EmbeddingRequest
from info.utils.Authentication import verify_token
from info.utils.api_servers.llm_base import servers_embedding_text

router = APIRouter()


@router.api_route(path='/ai/embedding/model/list', methods=['GET'], summary="获取支持的embedding模型列表")
@limiter.limit(API_LIMIT['model_list'])
def support_embedding_model_list(request: Request,
                                 user_id=Depends(verify_token)
                                 ):
    return JSONResponse({'data': [{'model_name': k, **v['info']} for k, v in Embedding_Models.items()]})


@router.api_route(path='/ai/embedding/text', methods=['POST'], summary="文本embedding")
@limiter.limit(API_LIMIT['text_embedding'])
def text_embedding(request: Request,
                   req: EmbeddingRequest,
                   user_id=Depends(verify_token)
                   ):
    logger.info(req.dict())

    return JSONResponse(servers_embedding_text(**req.dict()).json())
