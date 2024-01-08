# *_*coding:utf-8 *_*
# @Author : YueMengRui
########################
API_OCR_GENERAL = 'http://paimongpt_ocr_center:24666/ai/ocr/general'
API_TABLE_ANALYSIS = 'http://paimongpt_ocr_center:24666/ai/table/analysis'
API_LAYOUT_ANALYSIS = 'http://paimongpt_tools_server:24614/ai/layout/analysis'
########################

TOKENIZE_APIS_URL_PREFIX = 'http://paimongpt_tokenizer_server:24612'
TOKENIZE_APIS = {
    'word_seg': TOKENIZE_APIS_URL_PREFIX + '/ai/tokenize/word_seg',
    'add_keywords': TOKENIZE_APIS_URL_PREFIX + '/ai/tokenize/keywords/add',
    'add_stopwords': TOKENIZE_APIS_URL_PREFIX + '/ai/tokenize/stopwords/add'
}
########################
# LLM Configs
LLM_SERVER_APIS = {
    'token_counter': '/ai/llm/token_count',
    'chat': '/ai/llm/chat',
}
########################

QWENVL_CHAT = 'http://qwenvl:24610/ai/llm/chat/qwenvl'

########################
# Embedding Configs
EMBEDDING_SERVER_APIS = {
    'embedding_text': '/ai/embedding/text',
    'embedding_token_count': '/ai/embedding/token/count',
}
########################
