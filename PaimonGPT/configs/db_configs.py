# *_*coding:utf-8 *_*
# @Author : YueMengRui
########################
# Mysql Configs
MYSQL_HOST = 'paimongpt_mysql'
MYSQL_POST = 3306
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = '666666'
MYSQL_DATABASE_NAME = 'paimongpt'
########################

########################
# Milvus Configs
MILVUS_HOST = 'paimongpt_milvus'
MILVUS_PORT = 19530
MILVUS_DB_NAME = 'paimongpt'
MILVUS_USERNAME = ''
MILVUS_PASSWORD = ''
########################

DBQA_PRESETS = {
    'paimongpt': {
        'host': MYSQL_HOST,
        'port': MYSQL_POST,
        'username': MYSQL_USERNAME,
        'password': MYSQL_PASSWORD,
        'db_name': 'paimongpt'
    }
}
