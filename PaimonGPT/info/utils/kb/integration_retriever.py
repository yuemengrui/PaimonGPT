# *_*coding:utf-8 *_*
# @Author : YueMengRui
from info.utils.kb.Retriever import multiquery_retriever, bm25_retriever


def retrieve_data(query, llm_name, embedding_model, text_hash_list):
    queries, docs, context = multiquery_retriever(query, llm_name, embedding_model, text_hash_list)

    bm25_retriever.search(query, docs)
