# *_*coding:utf-8 *_*
# @Author : YueMengRui
import time
import math
import requests
import numpy as np
from typing import List
from mylogger import logger
from configs import TOKENIZE_APIS


class BM25:
    def __init__(self, k1=1.5, b=0.75, epsilon=0.25, **kwargs):
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon

    def _initialize(self, corpus: List[List[str]]):
        nd = {}  # word -> number of documents with word
        num_doc = 0
        corpus_size = 0  # 总文档数
        doc_len = []
        doc_freqs = []
        for document in corpus:
            doc_len.append(len(document))
            num_doc += len(document)

            frequencies = {}
            for word in document:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1
            doc_freqs.append(frequencies)

            for word, freq in frequencies.items():
                try:
                    nd[word] += 1
                except KeyError:
                    nd[word] = 1

            corpus_size += 1

        avgdl = num_doc / corpus_size  # 平均文档长度
        return nd, corpus_size, doc_len, doc_freqs, avgdl

    def _calc_idf(self, nd, corpus_size):
        """
        Calculates frequencies of terms in documents and in corpus.
        This algorithm sets a floor on the idf values to eps * average_idf
        """
        # collect idf sum to calculate an average idf for epsilon value
        IDF = {}
        idf_sum = 0
        # collect words with negative idf to set them a special epsilon value.
        # idf can be negative if word is contained in more than half of documents
        negative_idfs = []
        for word, freq in nd.items():
            idf = math.log(corpus_size - freq + 0.5) - math.log(freq + 0.5)
            IDF[word] = idf
            idf_sum += idf
            if idf < 0:
                negative_idfs.append(word)
        self.average_idf = idf_sum / len(IDF)

        eps = self.epsilon * self.average_idf
        for word in negative_idfs:
            IDF[word] = eps

        return IDF

    def get_scores(self, query, corpus_size, doc_len, doc_freqs, idf, avgdl):
        """
        The ATIRE BM25 variant uses an idf function which uses a log(idf) score. To prevent negative idf scores,
        this algorithm also adds a floor to the idf value of epsilon.
        See [Trotman, A., X. Jia, M. Crane, Towards an Efficient and Effective Search Engine] for more info
        """
        score = np.zeros(corpus_size)
        doc_len = np.array(doc_len)
        for q in query:
            q_freq = np.array([(doc.get(q) or 0) for doc in doc_freqs])
            score += (idf.get(q) or 0) * (q_freq * (self.k1 + 1) /
                                          (q_freq + self.k1 * (1 - self.b + self.b * doc_len / avgdl)))
        return score

    def get_top_k(self, query, corpus, k=10):
        nd, corpus_size, doc_len, doc_freqs, avgdl = self._initialize(corpus)
        idf = self._calc_idf(nd, corpus_size)

        scores = self.get_scores(query, corpus_size, doc_len, doc_freqs, idf, avgdl)
        top_n = np.argsort(scores)[::-1][:k]
        return top_n.tolist(), scores[top_n].tolist()


class BM25Retriever:

    def __init__(self, **kwargs):
        self.bm25 = BM25()

    @staticmethod
    def word_seg(texts: List[str], return_origin=False, return_completion=False, every_completion_limit=5, **kwargs):
        req_data = {
            "texts": texts,
            "return_origin": return_origin,
            "return_completion": return_completion,
            "every_completion_limit": every_completion_limit
        }

        try:
            resp = requests.post(url=TOKENIZE_APIS['word_seg'], json=req_data).json()['data']
            return resp
        except Exception as e:
            return []

    def search(self, query: str, texts: List[str], text_hash: List[str], k=10, **kwargs):
        time_cost = {'total': '0s'}
        start = time.time()
        corpus = self.word_seg(texts)
        if len(corpus) == 0:
            return [], time_cost

        query_seg = self.word_seg([query], return_completion=True)
        if len(query_seg) == 0:
            return [], time_cost

        query_seg = query_seg[0]

        top_n_index, scores = self.bm25.get_top_k(query=query_seg, corpus=corpus, k=k)

        related_texts = []
        for i in range(len(top_n_index)):
            related_texts.append(
                {'text': texts[top_n_index[i]], 'text_hash': text_hash[top_n_index[i]], 'score': scores[i]})

        logger.info({"bm25_retriever_related_texts": related_texts})
        time_cost.update({'total': f"{time.time() - start:.3f}s"})
        return related_texts, time_cost
