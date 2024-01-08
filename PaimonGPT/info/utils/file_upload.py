# *_*coding:utf-8 *_*
# @Author : YueMengRui
import requests
from mylogger import logger
from typing import Union
from configs import UPLOAD_FILE_URL


def upload_file(file: Union[str, bytes], file_name: str):
    if isinstance(file, str):
        file = open(file, 'rb')

    try:
        resp = requests.post(url=UPLOAD_FILE_URL,
                             files={"file": (file_name, file)})
        return resp.json()['file_url']
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return None
