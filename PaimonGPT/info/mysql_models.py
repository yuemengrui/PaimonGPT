# *_*coding:utf-8 *_*
# @Author : YueMengRui
import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, TEXT, JSON
from .db_mysql import Base


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = Column(DateTime, default=datetime.datetime.now, comment="记录的创建时间")
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                         comment="记录的更新时间")


class FileSystem(Base, BaseModel):
    __tablename__ = 'file_system'
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
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True, index=True)
    password = Column(String(256), nullable=False)


class SystemApp(Base, BaseModel):
    __tablename__ = 'system_app'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    is_delete = Column(Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class App(Base, BaseModel):
    __tablename__ = 'app'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(32), nullable=False)
    llm_name = Column(String(32))
    is_system = Column(Boolean, default=False, comment='是否是系统应用')
    system_app_id = Column(Integer, comment='系统应用id')
    is_delete = Column(Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "llm_name": self.llm_name,
            "is_system": self.is_system
        }


class App_KB(Base, BaseModel):
    __tablename__ = 'app_kb'
    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, nullable=False)
    kb_id = Column(Integer, nullable=False)
    kb_name = Column(String(32), nullable=False)


class ChatRecord(Base, BaseModel):
    __tablename__ = 'chat_record'
    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, nullable=False)
    name = Column(String(16))
    dynamic_name = Column(String(16))
    is_delete = Column(Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "app_id": self.app_id,
            "name": self.name if self.name else self.dynamic_name
        }


class ChatMessageRecord(Base, BaseModel):
    __tablename__ = 'chat_message_record'
    id = Column(Integer, primary_key=True)
    uid = Column(String(64), nullable=False)
    chat_id = Column(Integer, nullable=False)
    role = Column(String(32), default='assistant', nullable=False)
    content = Column(TEXT)
    type = Column(String(16), default='text', comment='消息类型：text image')
    url = Column(String(256))
    response = Column(JSON, default={})
    llm_name = Column(String(32))
    is_delete = Column(Boolean, default=False)

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
    __tablename__ = 'kb'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(32), nullable=False)
    embedding_model = Column(String(32), nullable=False)
    is_delete = Column(Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "embedding_model": self.embedding_model
        }


class KBFile(Base, BaseModel):
    __tablename__ = 'kb_file'
    id = Column(Integer, primary_key=True)
    kb_id = Column(Integer, nullable=False)
    method_id = Column(Integer, nullable=False, comment='1:自动分段，2:QA拆分， 3:json导入')
    file_name = Column(String(128), nullable=False)
    file_hash = Column(String(64), nullable=False)
    file_type = Column(String(256))
    file_size = Column(Integer, default=0)
    file_url = Column(String(256))
    chunk_total = Column(Integer, default=0)
    is_disable = Column(Boolean, default=False)
    is_delete = Column(Boolean, default=False)

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
    __tablename__ = 'kb_file_chunks'
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, nullable=False)
    type = Column(String(16), nullable=False)  # text, table, figure
    page = Column(String(16))
    content = Column(TEXT)
    content_hash = Column(String(64))
    url = Column(String(512), comment="图片url")
    html = Column(TEXT)

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "page": self.page,
            "content": self.content,
            "content_hash": self.content_hash,
            "url": self.url,
            "html": self.html
        }
