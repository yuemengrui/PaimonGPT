# *_*coding:utf-8 *_*
# @Author : YueMengRui
import time
from mylogger import logger
from info import milvus_db
from info.utils.common import paser_str_to_json
from info.utils.kb.rrf import reciprocal_rank_fusion
from info.utils.api_servers.llm_base import servers_llm_chat, servers_embedding_text
from configs.prompt_template import multiqueryretriever_prompt_template


def multiquery_retriever(query, llm_name, embedding_model, text_hash_list):
    time_cost = {}
    t1 = time.time()
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

    t2 = time.time()
    time_cost.update({'multiquery_generate': f"{t2 - t1:.3f}s"})

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

    texts = []
    for i in range(len(embeddings)):
        texts.append(milvus_db.similarity_search(embedding_model, embeddings[i], expr=f"text_hash in {text_hash_list}"))

    t3 = time.time()
    time_cost.update({'multiquery_retrieve': f"{t3 - t2:.3f}s"})
    related_texts = reciprocal_rank_fusion(texts, weights)

    logger.info(f"multiquery_retriever: related texts: {related_texts}")

    time_cost.update({'total': f"{time.time() - t1:.3f}s"})
    return queries, related_texts, time_cost
