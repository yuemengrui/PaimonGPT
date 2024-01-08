# *_*coding:utf-8 *_*
# @Author : YueMengRui
import requests
from mylogger import logger
from info.utils.common import cv2_to_base64
from configs import API_OCR_GENERAL


def get_ocr_general_res(img, return_str=False, **kwargs):
    data = {
        'image': cv2_to_base64(img)
    }

    data.update(kwargs)

    try:
        res = requests.post(url=API_OCR_GENERAL,
                            json=data)

        if return_str:
            txt_list = [x['text'][0] for x in res.json()['data']]
            return ''.join(txt_list)

        return res.json()['data']

    except Exception as e:
        logger.error({'EXCEPTION': e})
        return None
