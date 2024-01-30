# *_*coding:utf-8 *_*
# @Author : YueMengRui
from typing import List
from mylogger import logger


def reciprocal_rank_fusion(texts: List, weights: List = None, k=60, score_threshold=0.01):
    """
    Args:
        texts: [[{'text': 'xx', 'text_hash': 'xx'}, {}], [], []]
        weights: weights.length should be == texts.length
        k:
        score_threshold:

    Returns: [{'text': 'xx', 'text_hash': 'xx'}, {}]
    """
    rerank_texts = {}

    if not isinstance(weights, list) or len(weights) != len(texts):
        weights = [1] * len(texts)

    for i in range(len(weights)):
        for rank, text in enumerate(texts[i]):

            if text['text_hash'] not in rerank_texts:
                text.update({'score': 0})
                rerank_texts[text['text_hash']] = text

            rerank_texts[text['text_hash']]['score'] += weights[i] * (1 / (rank + k))

    related_texts = list(rerank_texts.values())

    related_texts.sort(key=lambda x: x['score'], reverse=True)
    logger.info(f"rrf: related texts: {related_texts}")

    return [x for x in related_texts if x['score'] > score_threshold]
