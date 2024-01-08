# *_*coding:utf-8 *_*
# @Author : YueMengRui
import re
import json
from mylogger import logger
from info import milvus_db
from info.utils.common import paser_str_to_json
from info.utils.api_servers.llm_base import servers_llm_chat, servers_embedding_text
from configs.prompt_template import multiqueryretriever_prompt_template


def reciprocal_rank_fusion(docs, weights, k=60, score_threshold=0.01):
    rerank_docs = {}

    for i in range(len(weights)):
        for rank, doc in enumerate(docs[i]):

            if doc['text_hash'] not in rerank_docs:
                doc.update({'score': 0})
                rerank_docs[doc['text_hash']] = doc

            rerank_docs[doc['text_hash']]['score'] += weights[i] * (1 / (rank + k))

    related_docs = list(rerank_docs.values())

    related_docs.sort(key=lambda x: x['score'], reverse=True)
    logger.info(f"multiquery_retriever: related docs: {related_docs}")

    return [x for x in related_docs if x['score'] > score_threshold]


def multiquery_retriever(query, llm_name, embedding_model, text_hash_list):
    queries = [query]
    resp = servers_llm_chat(prompt=multiqueryretriever_prompt_template.format(query=query), model_name=llm_name)
    logger.info(f"multiquery_retriever: {resp}")
    resp_json_data = None
    if resp:
        resp_json_data = paser_str_to_json(resp)

    if resp_json_data:
        logger.info(f"multiquery_retriever: json: {resp_json_data}")

        for i in list(resp_json_data.values()):
            if isinstance(i, str) and (i not in queries):
                queries.append(i)

    weight = 1 / (len(queries) + 1)
    weights = [weight] * len(queries)
    weights[0] = (2 * weight)
    logger.info(f"queries: {queries}")
    logger.info(f"weights: {weights}")

    if embedding_model == 'bge_large_zh':
        sentences = ["为这个句子生成表示以用于检索相关文章：" + q for q in queries]
    else:
        sentences = queries

    embeddings = servers_embedding_text(sentences=sentences, model_name=embedding_model).json()['embeddings']

    docs = []
    for i in range(len(embeddings)):
        docs.append(milvus_db.similarity_search(embedding_model, embeddings[i], expr=f"text_hash in {text_hash_list}"))

    related_docs = reciprocal_rank_fusion(docs, weights)

    logger.info(f"multiquery_retriever: related docs: {related_docs}")
    front = []
    back = []
    flag = 'front'

    for doc in related_docs:
        if flag == 'front':
            front.append(doc['text'])
            flag = 'back'
        else:
            back.insert(0, doc['text'])
            flag = 'front'

    context = '\n'.join(front + back)
    logger.info(f"multiquery_retriever: context: {context}")

    return queries, related_docs, context
