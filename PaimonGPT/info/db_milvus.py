# *_*coding:utf-8 *_*
# @Author : YueMengRui
import numpy as np
from configs import MILVUS_HOST, MILVUS_PORT, MILVUS_USERNAME, MILVUS_PASSWORD, MILVUS_DB_NAME
from pymilvus import CollectionSchema, FieldSchema, DataType, Collection, MilvusException, connections, db, utility


def sigmoid_normalize_distance(distance, scale=1):
    normalized_distance = float(1 / (1 + np.exp(scale * distance))) + 0.5
    return 1 if normalized_distance > 1 else normalized_distance


class MilvusDB:

    def __init__(self, logger=None):
        self.logger = logger
        self.collections = {}
        self._connect()

    def _connect(self):
        connections.connect(
            user=MILVUS_USERNAME,
            password=MILVUS_PASSWORD,
            host=MILVUS_HOST,
            port=MILVUS_PORT
        )

        db_list = db.list_database()
        self.logger.info(f"milvus: db list: {db_list}")

        if MILVUS_DB_NAME not in db_list:
            db.create_database(MILVUS_DB_NAME)

        db.using_database(MILVUS_DB_NAME)

        connections.connect(
            user=MILVUS_USERNAME,
            password=MILVUS_PASSWORD,
            host=MILVUS_HOST,
            port=MILVUS_PORT,
            db_name=MILVUS_DB_NAME
        )

    def _create_collection(self, collection_name: str, embedding: list):
        schema = CollectionSchema(
            enable_dynamic_field=True,
            description=collection_name,
            fields=[
                FieldSchema(name='text', dtype=DataType.VARCHAR, max_length=16 * 1024),
                FieldSchema(name='text_hash', dtype=DataType.VARCHAR, max_length=64, is_primary=True),
                FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=len(embedding)),
            ]
        )

        # Create the collection
        try:
            col = Collection(
                name=collection_name,
                schema=schema,
                consistency_level="Session"
            )

            col.create_index(field_name='text_hash', index_name='text_hash')
            col.create_index(field_name='embedding', index_params={
                "metric_type": "L2",
                "index_type": "FLAT"
            })
        except MilvusException as e:
            self.logger.error(f"Failed to create collection: {collection_name} error:{e}")
            return None
        else:
            col.load()
            self.collections.update({collection_name: col})
            return col

    def get_collection(self, collection_name, embedding, create=False):
        if collection_name in self.collections:
            return self.collections[collection_name]
        else:
            if utility.has_collection(collection_name):
                col = Collection(collection_name)
                col.load()
                self.collections.update({collection_name: col})
                return col
            else:
                if create:
                    return self._create_collection(collection_name, embedding)
                else:
                    return None

    # def insert_data(self, collection_name, texts: list, text_hashs: list, embeddings: list):
    #     self.logger.info(f"start insert data......")
    #     col = self.get_collection(collection_name, embeddings[0], create=True)
    #     self.logger.info(col)
    #     if col is None:
    #         return False
    #     try:
    #         col.insert([texts, text_hashs, embeddings])
    #         col.flush()
    #     except Exception as e:
    #         self.logger.error({'EXCEPTION': e})
    #         return False
    #
    #     return True

    def upsert_data(self, collection_name, texts: list, text_hashs: list, embeddings: list):
        self.logger.info(f"start insert data......")
        col = self.get_collection(collection_name, embeddings[0], create=True)
        if col is None:
            return False
        try:
            col.upsert([texts, text_hashs, embeddings])
            col.flush()
        except Exception as e:
            self.logger.error({'EXCEPTION': e})
            return False

        return True

    def similarity_search(self, collection_name, query_embedding, k=10, param=None, expr=None,
                          timeout=None, threshold=0.1, **kwargs):
        if param is None:
            param = {"metric_type": "L2"}

        res = []

        col = self.get_collection(collection_name, query_embedding)
        if col is None:
            return res

        results = col.search(
            data=[query_embedding],
            anns_field='embedding',
            param=param,
            limit=k,
            expr=expr,
            output_fields=['text', 'text_hash'],
            timeout=timeout,
            **kwargs,
        )

        self.logger.info(f"milvus search result: {results}")
        hash_filter = []
        for i in results[0]:
            text_hash = i.entity.get('text_hash')
            if text_hash not in hash_filter:
                hash_filter.append(text_hash)
                res.append({'text': i.entity.get('text'), 'text_hash': text_hash, 'distance': i.distance})
                # res.append({'text': i.entity.get('text'), 'text_hash': text_hash, 'distance': i.distance,
                #             'score': sigmoid_normalize_distance(i.distance)})
        self.logger.info(f"milvus search result: {res}")
        # res.sort(key=lambda x: x['score'], reverse=True)
        # if threshold:
        #     res = [x for x in res if x['score'] >= threshold]
        # self.logger.info(f"milvus search result: {res}")
        return res
