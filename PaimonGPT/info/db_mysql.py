# *_*coding:utf-8 *_*
# @Author : YueMengRui
from configs import MYSQL_HOST, MYSQL_POST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE_NAME
from urllib import parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 数据库连接配置
SQLALCHEMY_DATABASE_URI = (
    "mysql+pymysql://{}:{}@{}:{}/{}".format(MYSQL_USERNAME, parse.quote_plus(MYSQL_PASSWORD), MYSQL_HOST, MYSQL_POST,
                                            MYSQL_DATABASE_NAME)
)

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URI)
# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 声明基类
Base = declarative_base()
