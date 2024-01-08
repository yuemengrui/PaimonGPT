# *_*coding:utf-8 *_*
# @Author : YueMengRui
import requests
from mylogger import logger
from typing import List
from info import LLM_Models, Embedding_Models
from configs import LLM_SERVER_APIS, EMBEDDING_SERVER_APIS


def servers_llm_chat(prompt, model_name, history: list = [], generation_configs: dict = {}):
    req_data = {
        "prompt": prompt,
        "history": history,
        "generation_configs": generation_configs,
        "stream": False
    }
    resp = requests.post(url=LLM_Models[model_name]['url_prefix'] + LLM_SERVER_APIS['chat'], json=req_data)
    try:
        return resp.json()['answer']
    except Exception as e:
        logger.info(resp.text, e)
        return None


def servers_token_count(prompt: str, model_name: str):
    req_data = {
        "prompt": prompt
    }

    return requests.post(url=LLM_Models[model_name]['url_prefix'] + LLM_SERVER_APIS['token_counter'], json=req_data)


def servers_embedding_text(sentences: List[str], model_name: str):
    req_data = {
        "model_name": model_name,
        "sentences": sentences
    }

    return requests.post(url=Embedding_Models[model_name]['url_prefix'] + EMBEDDING_SERVER_APIS['embedding_text'],
                         json=req_data)
