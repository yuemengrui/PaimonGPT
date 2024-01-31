# *_*coding:utf-8 *_*
# @Author : YueMengRui
import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, TEXT, JSON, BIGINT
from .db_mysql import Base


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = Column(DateTime, default=datetime.datetime.now, comment="记录的创建时间")
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                         comment="记录的更新时间")


class FileSystem(Base, BaseModel):
    __tablename__ = 'file_system'
    __table_args__ = {'comment': '文件系统表'}
    id = Column(Integer, primary_key=True)
    file_hash = Column(String(64), nullable=False, index=True)
    file_type = Column(String(256))
    file_ext = Column(String(32))
    file_size = Column(Integer, default=0)
    base_dir = Column(String(256))


class UserFileSystem(Base, BaseModel):
    __tablename__ = 'user_file_system'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    file_hash = Column(String(64), nullable=False, index=True)
    file_name = Column(String(256))
    file_type = Column(String(256))
    file_size = Column(Integer, default=0)
    base_dir = Column(String(256))


class User(Base, BaseModel):
    __tablename__ = 'user'
    __table_args__ = {'comment': '用户表'}
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True, index=True, comment="用户名")
    password = Column(String(256), nullable=False)


class AppStore(Base, BaseModel):
    __tablename__ = 'appstore'
    __table_args__ = {'comment': '应用商城中的应用表'}
    id = Column(Integer, primary_key=True)
    uid = Column(BIGINT, nullable=False, unique=True, comment="唯一id")
    name = Column(String(16), nullable=False, comment="应用名")
    description = Column(String(256), comment="应用描述")
    module_name = Column(String(64), nullable=False)
    is_installed = Column(Boolean, default=True, comment="应用是否已上架到商城，0表示已下架，1表示已上架")

    def to_dict(self):
        return {
            "id": self.uid,
            "name": self.name,
            "description": self.description
        }


class App(Base, BaseModel):
    __tablename__ = 'app'
    __table_args__ = {'comment': '用户的应用表'}
    id = Column(Integer, primary_key=True)
    uid = Column(BIGINT, nullable=False, unique=True, comment="唯一id")
    user_id = Column(Integer, nullable=False, comment="用户id")
    name = Column(String(32), nullable=False, comment="应用名称")
    llm_name = Column(String(32), comment="应用关联的大模型名")
    description = Column(String(256), comment="应用描述")
    is_appstore = Column(Boolean, default=False, comment='是否是商城应用')
    appstore_uid = Column(BIGINT, comment='商城应用唯一id')
    is_delete = Column(Boolean, default=False, comment="是否被删除，1表示已被删除，0表示未删除")

    def to_dict(self):
        return {
            "id": self.uid,
            "name": self.name,
            "llm_name": self.llm_name,
            "description": self.description,
            "is_appstore": self.is_appstore,
            "appstore_uid": self.appstore_uid
        }


class App_KB(Base, BaseModel):
    __tablename__ = 'app_knowledgebase'
    __table_args__ = {'comment': '应用与知识库关联表'}
    id = Column(Integer, primary_key=True)
    app_id = Column(BIGINT, nullable=False, comment="应用的唯一id")
    kb_id = Column(BIGINT, nullable=False, comment="知识库的唯一id")
    kb_name = Column(String(32), nullable=False, comment="知识库名")


class ChatRecord(Base, BaseModel):
    __tablename__ = 'chat_record'
    __table_args__ = {'comment': '应用的对话表'}
    id = Column(Integer, primary_key=True)
    app_id = Column(BIGINT, nullable=False, comment="应用的唯一id")
    name = Column(String(16), comment="对话名")
    dynamic_name = Column(String(16))
    is_delete = Column(Boolean, default=False, comment="是否被删除，1表示已被删除，0表示未删除")

    def to_dict(self):
        return {
            "id": self.id,
            "app_id": self.app_id,
            "name": self.name if self.name else self.dynamic_name
        }


class ChatMessageRecord(Base, BaseModel):
    __tablename__ = 'chat_message_record'
    __table_args__ = {'comment': '对话中的消息表'}
    id = Column(Integer, primary_key=True)
    uid = Column(String(64), nullable=False, comment="唯一id")
    chat_id = Column(Integer, nullable=False, comment="对话表的id")
    role = Column(String(32), default='assistant', nullable=False, comment="角色")
    content = Column(TEXT, comment="消息的内容")
    type = Column(String(16), default='text', comment='消息类型：text image')
    url = Column(String(256))
    response = Column(JSON, default={})
    llm_name = Column(String(32))
    is_delete = Column(Boolean, default=False, comment="是否被删除，1表示已被删除，0表示未删除")

    def to_dict(self):
        return {
            "id": self.uid,
            "uid": self.uid,
            "chat_id": self.chat_id,
            "role": self.role,
            "type": self.type,
            "url": self.url,
            "content": self.content,
            "response": self.response,
            "llm_name": self.llm_name
        }


class MultiQueryRetriever(Base, BaseModel):
    __tablename__ = 'multiquery_retriever'
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, nullable=False)
    origin_query = Column(TEXT, nullable=False)
    generate_query = Column(TEXT, nullable=False)


class KB(Base, BaseModel):
    __tablename__ = 'knowledgebase'
    __table_args__ = {'comment': '知识库表'}
    id = Column(Integer, primary_key=True)
    uid = Column(BIGINT, nullable=False, unique=True, comment="唯一id")
    user_id = Column(Integer, nullable=False, comment="用户id")
    name = Column(String(32), nullable=False, comment="知识库名")
    description = Column(String(256), comment="知识库描述")
    embedding_model = Column(String(32), nullable=False, comment="知识库关联的embedding模型")
    is_delete = Column(Boolean, default=False, comment="是否被删除，1表示已被删除，0表示未删除")

    def to_dict(self):
        return {
            "id": self.uid,
            "name": self.name,
            "embedding_model": self.embedding_model,
            "description": self.description
        }


class KBFile(Base, BaseModel):
    __tablename__ = 'knowledgebase_file'
    __table_args__ = {'comment': '知识库中的文件表'}
    id = Column(Integer, primary_key=True)
    kb_id = Column(BIGINT, nullable=False)
    method_id = Column(Integer, nullable=False, comment='1:自动分段，2:QA拆分， 3:json导入')
    file_name = Column(String(128), nullable=False)
    file_hash = Column(String(64), nullable=False)
    file_type = Column(String(256))
    file_size = Column(Integer, default=0)
    file_url = Column(String(256))
    chunk_total = Column(Integer, default=0)
    is_disable = Column(Boolean, default=False)
    is_delete = Column(Boolean, default=False, comment="是否被删除，1表示已被删除，0表示未删除")

    def to_dict(self):
        return {
            "id": self.id,
            "method_id": self.method_id,
            "file_name": self.file_name,
            "file_hash": self.file_hash,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "file_url": self.file_url,
            "chunk_total": self.chunk_total,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "is_disable": self.is_disable
        }


class KBFileChunks(Base, BaseModel):
    __tablename__ = 'knowledgebase_file_chunks'
    __table_args__ = {'comment': '知识库文件的chunk表'}
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, nullable=False)
    type = Column(String(16), nullable=False)  # text, table, figure
    page = Column(String(16))
    content = Column(TEXT)
    children = Column(JSON)
    url = Column(String(512), comment="图片url")
    html = Column(TEXT)

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "page": self.page,
            "content": self.content,
            "url": self.url,
            "html": self.html
        }


class DBQADB(Base, BaseModel):
    __tablename__ = 'dbqa_db'
    __table_args__ = {'comment': '数据库问答数据库表'}
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, comment="用户id")
    chat_id = Column(Integer, comment="对话id")
    host = Column(String(16), nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String(32), nullable=False)
    db_name = Column(String(64), nullable=False)


class DBQADBTableDescription(Base, BaseModel):
    __tablename__ = 'dbqa_db_table_description'
    __table_args__ = {'comment': '数据库问答数据库表描述'}
    id = Column(Integer, primary_key=True)
    db_id = Column(Integer, nullable=False, comment="数据库id")
    table_name = Column(String(32), nullable=False)
    table_comment = Column(String(512))
    columns = Column(JSON, default=[])
    is_deprecated = Column(Boolean, default=False, comment="是否弃用")
    examples = Column(JSON)
