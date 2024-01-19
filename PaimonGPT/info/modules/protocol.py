# *_*coding:utf-8 *_*
# @Author : YueMengRui
from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Union


class ErrorResponse(BaseModel):
    errcode: int
    errmsg: str


class ModelRegisterRequest(BaseModel):
    type: str = Literal['llm', 'embedding']
    model_name: str
    url_prefix: str
    info: dict = Field(default={})


class FileUploadResponse(BaseModel):
    file_hash: str
    file_url: str
    file_name: str = Field(default=None)
    file_size: int
    file_type: str = Field(default=None)
    file_ext: str = Field(default='')


class AuthRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    token: str
    expires: int


class ChatRequest(BaseModel):
    app_id: int
    chat_id: int
    uid: str
    answer_uid: str
    model_name: str = Field(default=None, description="模型名称")
    prompt: str
    history: List = Field(default=[], description="历史记录")
    generation_configs: Dict = {}
    stream: bool = Field(default=True, description="是否流式输出")
    custom: Dict = Field(default={})
    """
    :param custom: {
                "tableQA": {
                    "table_content": ""
                }
            }
    """


class ChatVLImageRequest(BaseModel):
    app_id: int
    chat_id: int
    uid: str
    model_name: str = Field(default="Qwen_VL", description="模型名称")
    url: str


class ChatVLRequest(BaseModel):
    app_id: int
    chat_id: int
    uid: str
    answer_uid: str
    model_name: str
    prompt: str
    history: List = Field(default=[], description="历史记录")
    generation_configs: Dict = Field(default={})
    stream: bool = Field(default=True, description="是否流式输出")
    true_prompt: List


class ChatResponse(BaseModel):
    model_name: str
    answer: str
    history: List[List[str]]
    usage: Dict


class ChatSimpleRequest(BaseModel):
    model_name: str = Field(default=None, description="模型名称")
    prompt: str
    history: List = Field(default=[], description="历史记录")
    generation_configs: Dict = {}
    stream: bool = Field(default=True, description="是否流式输出")


class EmbeddingRequest(BaseModel):
    model_name: str = Field(default=None, description="模型名称")
    sentences: List[str] = Field(description="句子列表")


class TokenCountRequest(BaseModel):
    model_name: str = Field(default=None, description="模型名称")
    prompt: str


class AppStoreAppInstallRequest(BaseModel):
    name: str
    description: str = Field(default='')
    module_name: str


class AppStoreAppUninstallRequest(BaseModel):
    app_id: int


class AppInfoRequest(BaseModel):
    app_id: int


class AppInfoModifyRequest(BaseModel):
    app_id: int
    kbs: List = Field(default=[])
    name: str
    llm_name: str


class AppCreateRequest(BaseModel):
    name: str
    llm_name: str
    kbs: List = Field(default=[])


class AppCreateFromAppStoreRequest(BaseModel):
    app_id: int


class AppDeleteRequest(BaseModel):
    app_id: int


class AppChatListRequest(BaseModel):
    app_id: int


class AppChatCreateRequest(BaseModel):
    app_id: int
    name: str = Field(default=None)


class AppChatDeleteRequest(BaseModel):
    chat_id: int


class AppChatMessageListRequest(BaseModel):
    chat_id: int
    page: int = Field(default=1, description='第几页')
    page_size: int = Field(default=10, description='每页多少条数据')


class KBCreateRequest(BaseModel):
    name: str
    description: str = Field(default='')
    embedding_model: str


class KBDeleteRequest(BaseModel):
    kb_id: int


class KBDataListRequest(BaseModel):
    kb_id: int


class KBDataDetailRequest(BaseModel):
    data_id: int


class KBDataDeleteRequest(BaseModel):
    data_id: int


class KBDataImportOne(BaseModel):
    file_hash: str
    file_name: str
    file_url: str
    file_size: int
    file_type: str
    file_ext: str = Field(default='')


class KBDataImportRequest(BaseModel):
    method_id: int
    kb_id: int
    files: List[KBDataImportOne]


class TableAnalysisRequest(BaseModel):
    app_id: int
    chat_id: int
    uid: str
    file_hash: str
    file_url: str


class DBConnectRequest(BaseModel):
    preset: str = Field(default=None, description='预设的db name')
    host: str = Field(default=None, description='DB host')
    port: Union[int, str] = Field(default=3306, description='DB port')
    username: str = Field(default=None, description='DB username')
    password: str = Field(default=None, description='DB password')
    db_name: str = Field(default=None, description='DB name')


class DBChatRequest(BaseModel):
    db_name: str = Field(description='DB name')
    model_name: str = Field(description="模型名称")
    prompt: str
    history: List = Field(default=[], description="历史记录")
    generation_configs: Dict = {}
