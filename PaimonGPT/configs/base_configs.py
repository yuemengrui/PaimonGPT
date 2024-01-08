# *_*coding:utf-8 *_*
# @Author : YueMengRui
import os

FASTAPI_TITLE = 'PaimonGPT'
FASTAPI_HOST = '0.0.0.0'
FASTAPI_PORT = 24601

########################
# File System Configs
THIS_SERVER_URL = 'http://localhost:' + str(FASTAPI_PORT)  # 本服务地址
UPLOAD_FILE_URL = THIS_SERVER_URL + '/ai/file/upload/public'
FILE_SYSTEM_DIR = './file_system'
TEMP = './temp'
os.makedirs(FILE_SYSTEM_DIR, exist_ok=True)
os.makedirs(TEMP, exist_ok=True)
########################

LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

########################
# Auth Configs
SECRET_KEY = 'PaiMonGPT-YueMengRui'
USERNAME_FILTER = ['administer', 'administrator']
TOKEN_EXPIRES = 7 * 24 * 60 * 60  # token过期时间
########################
