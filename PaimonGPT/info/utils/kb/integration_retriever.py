# *_*coding:utf-8 *_*
# @Author : YueMengRui
from typing import List
from mylogger import logger
from configs.prompt_template import kb_qa_prompt_template
from info.utils.kb.rrf import reciprocal_rank_fusion
from info.utils.api_servers.llm_base import servers_token_count
from info.utils.kb.Retriever import multiquery_retriever, bm25_retriever


def retrieve_data(query, file_chunks_map, chunk_children_map, chunk_id_content_map, text_hash_list, text_list,
                  embedding_model, llm_name):
    """
    Args:
        query:
        file_chunks_map:
        chunk_children_map:
        chunk_id_content_map:
        text_hash_list:
        text_list:
        embedding_model:
        llm_name:

    Returns:
        prompt: str
        related_docs: List
        msg: Dict
    """
    queries, multiquery_related_texts, multiquery_time_cost = multiquery_retriever(query, llm_name, embedding_model,
                                                                                   text_hash_list)

    bm25_related_texts, bm25_time_cost = bm25_retriever.search(query, text_list, text_hash_list)

    rrf_related_texts = reciprocal_rank_fusion([multiquery_related_texts, bm25_related_texts])
    logger.info({"rrf_related texts": rrf_related_texts})

    msg = {'MultiQueryRetriever': {'queries': queries, 'time_cost': multiquery_time_cost},
           'BM25Retriever': {'time_cost': bm25_time_cost}}

    if len(rrf_related_texts) == 0:
        return query, [], msg

    related_chunk_ids = []
    for i in rrf_related_texts:
        for k, v in chunk_children_map.items():
            if i['text_hash'] in v:
                if k not in related_chunk_ids:
                    related_chunk_ids.append(k)

    select_chunk_ids = []
    select_chunks = []
    # chunk token calc
    token_count_resp = servers_token_count(prompt=kb_qa_prompt_template.format(query=query, context=''),
                                           model_name=llm_name)
    base_prompt_token_len = token_count_resp.get('prompt_tokens')
    max_prompt_len = token_count_resp.get('max_tokens')

    for c_id in related_chunk_ids:
        chunk_token_len = servers_token_count(prompt=chunk_id_content_map[c_id], model_name=llm_name).get(
            'prompt_tokens')

        if base_prompt_token_len + chunk_token_len > max_prompt_len:
            break

        select_chunk_ids.append(c_id)
        select_chunks.append(chunk_id_content_map[c_id])
        base_prompt_token_len += chunk_token_len

    logger.info({'final chunks': select_chunks})

    if len(select_chunks) == 0:
        return query, [], msg

    front = []
    back = []
    flag = 'front'

    for chunk in select_chunks:
        if flag == 'front':
            front.append(chunk)
            flag = 'back'
        else:
            back.insert(0, chunk)
            flag = 'front'

    context = '\n'.join(front + back)
    logger.info(f"context: {context}")

    prompt = kb_qa_prompt_template.format(query=query, context=context)

    temp_docs = {}
    for chunk_id in select_chunk_ids:
        file_info = file_chunks_map[chunk_id]

        if file_info['file_hash'] in temp_docs:
            temp_docs[file_info['file_hash']]['related_content'].append(chunk_id_content_map[chunk_id])
        else:
            file_info.update({'related_content': [chunk_id_content_map[chunk_id]]})
            temp_docs.update({file_info['file_hash']: file_info})

    related_docs = list(temp_docs.values())

    logger.info({'related_docs': related_docs})

    return prompt, related_docs, msg
