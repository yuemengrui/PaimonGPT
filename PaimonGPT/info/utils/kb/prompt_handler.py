# *_*coding:utf-8 *_*
# @Author : YueMengRui
from configs.prompt_template import kb_qa_prompt_template, tableQA_prompt_template
from info.mysql_models import App, KBFile, KBFileChunks, KB
from info.utils.kb.Retriever import multiquery_retriever, bm25_retriever


def get_kb_data(mysql_db, app_id):
    data_chunk_map = {}
    text_hash_list = []
    text_list = []
    embedding_model = None
    llm_name = None

    app = mysql_db.query(App).get(app_id)
    if app and app.kb_id:
        llm_name = app.llm_name
        kb = mysql_db.query(KB).get(app.kb_id)
        if kb:
            embedding_model = kb.embedding_model
            kb_file_list = mysql_db.query(KBFile).filter(KBFile.kb_id == app.kb_id, KBFile.is_delete == False).all()
            if kb_file_list:
                for kb_file in kb_file_list:
                    data_chunks = mysql_db.query(KBFileChunks).filter(KBFileChunks.data_id == kb_file.id).all()
                    if data_chunks:
                        for c in data_chunks:
                            if c.type == 'text' and c.content_hash is not None:
                                if c.content_hash not in text_hash_list:
                                    data_chunk_map.update({c.content_hash: kb_file.to_dict()})
                                    text_hash_list.append(c.content_hash)
                                    text_list.append(c.content)

    return data_chunk_map, text_hash_list, text_list, embedding_model, llm_name


def get_final_prompt(req, app_id, mysql_db):
    prompt = req.prompt
    related_docs = []
    msg = {}

    if 'tableQA' in req.custom:
        prompt = tableQA_prompt_template.format(query=prompt, context=req.custom['tableQA']['table_content'])
    else:
        data_chunk_map, text_hash_list, text_list, embedding_model, llm_name = get_kb_data(mysql_db, app_id)

        if len(data_chunk_map) > 0:
            queries, docs, context = multiquery_retriever(prompt, llm_name, embedding_model,
                                                          list(set(text_hash_list)))
            temp_docs = {}
            for d in docs:
                kb_dat = data_chunk_map[d['text_hash']]
                if kb_dat['file_hash'] in temp_docs:
                    temp_docs[kb_dat['file_hash']]['related_texts'].append(d)
                else:
                    kb_dat.update({'related_texts': [d]})
                    temp_docs.update({kb_dat['file_hash']: kb_dat})

            related_docs = list(temp_docs.values())
            msg.update({"MultiQueryRetriever": {"queries": queries}})
            prompt = kb_qa_prompt_template.format(query=prompt, context=context)

    return prompt, related_docs, msg
