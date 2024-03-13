# *_*coding:utf-8 *_*
from fastapi import FastAPI
from . import chat, auth, myapp, knowledge_base, embedding, file_system, table, vl, model_register, health, dbqa, appstore, chart


def register_router(app: FastAPI):
    app.include_router(router=chat.router, prefix="", tags=["Chat"])
    app.include_router(router=embedding.router, prefix="", tags=['Embedding'])
    app.include_router(router=auth.router, prefix="", tags=['Auth'])
    app.include_router(router=myapp.router, prefix="", tags=['App'])
    app.include_router(router=knowledge_base.router, prefix="", tags=['Knowledge Base'])
    app.include_router(router=file_system.router, prefix="", tags=['File System'])
    app.include_router(router=table.router, prefix="", tags=['Table'])
    app.include_router(router=vl.router, prefix="", tags=['VL'])
    app.include_router(router=model_register.router, prefix="", tags=['model register'])
    app.include_router(router=health.router, prefix="", tags=['health'])
    app.include_router(router=dbqa.router, prefix="", tags=['DB QA'])
    app.include_router(router=appstore.router, prefix="", tags=['App Store'])
    app.include_router(router=chart.router, prefix="", tags=['Chart'])
