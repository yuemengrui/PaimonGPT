# *_*coding:utf-8 *_*
# @Author : YueMengRui
import os
import cv2
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends
from info.utils.Authentication import verify_token
from info import logger, limiter, get_mysql_db
from configs import API_LIMIT
from .protocol import TableAnalysisRequest, ErrorResponse
from fastapi.responses import JSONResponse
from info.mysql_models import ChatMessageRecord, FileSystem
from info.utils.table_process import split_rows
from info.utils.response_code import RET, error_map
from info.utils.box_segmentation import get_box
from info.utils.ocr import get_ocr_general_res

router = APIRouter()


@router.api_route(path='/ai/table/analysis', methods=['POST'], summary="table analysis")
@limiter.limit(API_LIMIT['chat'])
def table_analysis(request: Request,
                   req: TableAnalysisRequest,
                   mysql_db: Session = Depends(get_mysql_db),
                   user_id=Depends(verify_token)
                   ):
    file = mysql_db.query(FileSystem).filter(FileSystem.file_hash == req.file_hash).first()
    if file:
        file_path = os.path.join(file.base_dir, file.file_hash[:2], file.file_hash[2:4], file.file_hash)

    origin_image = cv2.imread(file_path)

    try:
        origin_img, boxes = get_box(origin_image)
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return JSONResponse(ErrorResponse(errcode=RET.SERVERERR, errmsg=error_map[RET.SERVERERR]).dict(),
                            status_code=500)

    raw_boxes = split_rows(boxes)

    raw_text = []
    for raw in raw_boxes:
        temp_raw = []
        for box in raw:
            crop_img = origin_img[box[1]:box[3], box[0]:box[2]]
            ocr_res = get_ocr_general_res(crop_img, return_str=True)
            temp_raw.append(ocr_res)
        raw_text.append(' | '.join(temp_raw))

    table_content = '\n'.join(raw_text)

    new_message_user = ChatMessageRecord()
    new_message_user.chat_id = req.chat_id
    new_message_user.uid = req.uid
    new_message_user.role = 'user'
    new_message_user.type = 'image'
    new_message_user.url = req.file_url

    try:
        mysql_db.add(new_message_user)
        mysql_db.commit()
    except Exception as e:
        logger.error({'DB ERROR': e})
        mysql_db.rollback()
        return JSONResponse(ErrorResponse(errcode=RET.DBERR, errmsg=error_map[RET.DBERR]).dict(), status_code=500)

    return JSONResponse({'file_hash': req.file_hash,
                         'file_url': req.file_url,
                         'table_content': table_content})
