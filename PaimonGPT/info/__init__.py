# *_*coding:utf-8 *_*
import time
from mylogger import logger
from fastapi.requests import Request
from starlette.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from .db_mysql import SessionLocal, engine
from .mysql_models import Base
from .db_milvus import MilvusDB
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
import nltk

nltk.data.path = ['nltk_data'] + nltk.data.path

Base.metadata.create_all(bind=engine)

milvus_db = MilvusDB(logger=logger)

LLM_Models = {}
Embedding_Models = {}

DBs = {}


async def get_mysql_db():
    try:
        mysql_db = SessionLocal()
        yield mysql_db
    except Exception as e:
        logger.error(e)
    finally:
        mysql_db.close()


limiter = Limiter(key_func=lambda *args, **kwargs: '127.0.0.1')


def app_registry(app):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    @app.middleware("http")
    async def api_time_cost(request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        cost = time.time() - start
        logger.info(f'end request "{request.method} {request.url.path}" - {cost:.3f}s')
        return response

    app.mount("/static", StaticFiles(directory=f"static"), name="static")

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="/static/redoc.standalone.js",
        )

    from info.modules import register_router

    register_router(app)
