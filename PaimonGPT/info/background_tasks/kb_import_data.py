# *_*coding:utf-8 *_*
# @Author : YueMengRui
import os
import time
from mylogger import logger
from info import milvus_db
from info.utils.get_md5 import md5hex
from info.utils.common import cv2_to_bytes
from info.utils.file_upload import upload_file
from info.libs.Knowledge_Base.loader.file_loader import load_file
from info.utils.api_servers.llm_base import servers_embedding_text
from info.mysql_models import KB, KBFile, KBFileChunks, FileSystem


def auto_chunk(req, mysql_db, embedding_model):
    for fil in req.files:
        logger.info(f"background task: {fil.file_hash} import start......")
        file_system = mysql_db.query(FileSystem).filter(FileSystem.file_hash == fil.file_hash).first()
        if file_system is None:
            logger.error(f"background task: {fil.file_hash} import failed: file system query failed")
            continue

        local_file_path = os.path.join(file_system.base_dir, fil.file_hash[:2], fil.file_hash[2:4], fil.file_hash)

        if not os.path.exists(local_file_path):
            logger.error(
                f"background task: {fil.file_hash} import failed: file local path {local_file_path} not exist")
            continue
        file_ext = fil.file_name.lower().split('.')[-1]
        docs, text_spliter = load_file(filepath=local_file_path, ext=file_ext, embedding_model=embedding_model)
        logger.info(f"background task: {docs}")

        emb_sentences = []
        emb_sentences_hash = []
        total = len(docs)
        for chunk in docs:
            """
            chunk: {'type': 'text', 'content': 'xxx', 'page': None}
            """
            chunk.update({'children': None})
            if chunk['type'] == 'text':
                children_list = text_spliter.split_text(chunk['content'])
                children = []
                for child in children_list:
                    child_hash = md5hex(child.encode('utf-8'))
                    if child_hash != '':
                        children.append({'text': child, 'text_hash': child_hash})
                        emb_sentences.append(child)
                        emb_sentences_hash.append(child_hash)

                chunk.update({'children': children})
            elif chunk['type'] == 'table':
                # TODO table handle

                chunk.update(
                    {'url': upload_file(cv2_to_bytes(chunk['image']), str(time.time() * 1000000) + '.jpg')})
            elif chunk['type'] == 'figure':
                # TODO figure handle

                chunk.update(
                    {'url': upload_file(cv2_to_bytes(chunk['image']), str(time.time() * 1000000) + '.jpg')})

        logger.info(f'background task: insert into milvus start......')

        embedding_resp = servers_embedding_text(sentences=emb_sentences, model_name=embedding_model)

        embeddings = embedding_resp.json()['embeddings']

        start = 0
        inert_failed = 0
        while True:
            if start > len(emb_sentences):
                break

            if not milvus_db.upsert_data(collection_name=embedding_model,
                                         texts=emb_sentences[start:start + 100],
                                         text_hashs=emb_sentences_hash[start:start + 100],
                                         embeddings=embeddings[start:start + 100]):
                logger.error(f"background task: {fil.file_hash} import failed: milvus insert data failed!!!")
                inert_failed = 1
                break

            start = start + 100

        if inert_failed == 1:
            continue

        logger.info(f'background task: insert into milvus successful')

        new_kb_file = KBFile()
        new_kb_file.kb_id = req.kb_id
        new_kb_file.method_id = req.method_id
        new_kb_file.file_hash = fil.file_hash
        new_kb_file.file_name = fil.file_name
        new_kb_file.file_type = fil.file_type
        new_kb_file.file_size = fil.file_size
        new_kb_file.file_url = fil.file_url
        new_kb_file.chunk_total = total
        mysql_db.add(new_kb_file)
        mysql_db.flush()
        file_id = new_kb_file.id

        kb_data_detail_list = []
        for c in docs:
            new_chunk = KBFileChunks()
            new_chunk.page = c['page']
            new_chunk.file_id = file_id
            new_chunk.children = c['children']

            if c['type'] == 'text':
                new_chunk.type = 'text'
                new_chunk.content = c['content']
            elif c['type'] == 'table':
                new_chunk.type = 'table'
                new_chunk.content = c['table_caption']
                new_chunk.url = c['url']
                new_chunk.html = c['html']
            elif c['type'] == 'figure':
                new_chunk.type = 'figure'
                new_chunk.content = c['figure_caption']
                new_chunk.url = c['url']

            kb_data_detail_list.append(new_chunk)

        mysql_db.add_all(kb_data_detail_list)
        try:
            mysql_db.commit()
            logger.info(f"background task: {fil.file_hash} import successful")
        except Exception as e:
            logger.error({'DB ERROR': e})
            mysql_db.rollback()


def import_data_2_kb(req, mysql_db):
    logger.info('background task import data start......')
    kb = mysql_db.query(KB).filter(KB.uid == req.kb_id).first()
    if kb:
        if req.method_id == 1:
            auto_chunk(req, mysql_db, kb.embedding_model)
