# *_*coding:utf-8 *_*
# @Author : YueMengRui
from configs.prompt_template import kb_qa_prompt_template
from info.mysql_models import App, KBFile, KBFileChunks, KB, App_KB
from info.utils.kb.Retriever import multiquery_retriever, bm25_retriever
from info.utils.kb.integration_retriever import retrieve_data


def get_kb_data(mysql_db, app_id):
    file_chunks_map = {}  # {'chunk_id': file_info_dict}
    chunk_children_map = {}  # {'chunk_id': [children_text_hash_list]}
    chunk_id_content_map = {}  # {'chunk_id': 'chunk_content'}
    text_hash_list = []
    text_list = []
    embedding_model = None
    llm_name = None

    app = mysql_db.query(App).get(app_id)
    app_kbs = mysql_db.query(App_KB).filter(App_KB.app_id == app_id).all()
    if app and app_kbs:
        llm_name = app.llm_name
        for app_kb in app_kbs:
            kb = mysql_db.query(KB).filter(KB.uid == app_kb.kb_id).first()
            if kb:
                embedding_model = kb.embedding_model
                kb_file_list = mysql_db.query(KBFile).filter(KBFile.kb_id == app_kb.kb_id,
                                                             KBFile.is_delete == False).all()
                if kb_file_list:
                    for kb_file in kb_file_list:
                        data_chunks = mysql_db.query(KBFileChunks).filter(KBFileChunks.file_id == kb_file.id).all()
                        if data_chunks:
                            for c in data_chunks:
                                if c.type == 'text' and c.children is not None:
                                    file_chunks_map.update({c.id: kb_file.to_dict()})
                                    chunk_children_map.update({c.id: [x['text_hash'] for x in c.children]})
                                    chunk_id_content_map.update({c.id: c.content})
                                    for child in c.children:
                                        if child['text_hash'] not in text_hash_list:
                                            text_hash_list.append(child['text_hash'])
                                            text_list.append(child['text'])

                                # TODO table and figure handle

    return file_chunks_map, chunk_children_map, chunk_id_content_map, text_hash_list, text_list, embedding_model, llm_name


def get_final_prompt(req, app_id, mysql_db):
    prompt = req.prompt
    related_docs = []
    msg = {}

    file_chunks_map, chunk_children_map, chunk_id_content_map, text_hash_list, text_list, embedding_model, llm_name = get_kb_data(
        mysql_db,
        app_id)

    if len(file_chunks_map) > 0:
        prompt, related_docs, msg = retrieve_data(prompt, file_chunks_map, chunk_children_map, chunk_id_content_map,
                                                  text_hash_list, text_list, embedding_model, llm_name)

    return prompt, related_docs, msg
