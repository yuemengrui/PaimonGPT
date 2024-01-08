# *_*coding:utf-8 *_*
# @Author : YueMengRui
import re
import cv2
import json
import base64
import requests
import numpy as np
from mylogger import logger


class DotDict(dict):
    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        value = self[key]
        if isinstance(value, dict):
            value = DotDict(value)
        return value


def cv2_to_base64(image):
    return base64.b64encode(np.array(cv2.imencode('.jpg', image)[1]).tobytes()).decode('utf-8')


def base64_to_cv2(b64str: str):
    data = base64.b64decode(b64str.encode('utf-8'))
    data = np.frombuffer(data, np.uint8)
    data = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return data


def bytes_to_cv2(data: bytes):
    data = np.frombuffer(data, np.uint8)
    data = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return data


def cv2_to_bytes(image):
    return np.array(cv2.imencode('.jpg', image)[1]).tobytes()


def request_to_image(image: str, url: str):
    if image:
        try:
            return base64_to_cv2(image)
        except Exception as e:
            logger.error({'EXCEPTION': e})

    try:
        return bytes_to_cv2(requests.get(url).content)
    except Exception as e:
        logger.error({'EXCEPTION': e})

    return None


def resize_4096(img):
    scale = 1
    h, w = img.shape[:2]

    if max(h, w) > 4096:
        scale = 4096 / max(h, w)
        img = cv2.resize(img, dsize=None, fx=scale, fy=scale)

    return img, scale


def paser_str_to_json(data: str):
    try:
        return json.loads(data)
    except:
        pass

    result = re.search(r"```json(.*?)```", data, re.DOTALL)
    if result:
        try:
            return json.loads(result.group(1))
        except:
            pass

    result = re.search(r"{(.*?)}", data, re.DOTALL)
    if result:
        try:
            return json.loads('{' + result.group(1) + '}')
        except:
            pass

    return None
