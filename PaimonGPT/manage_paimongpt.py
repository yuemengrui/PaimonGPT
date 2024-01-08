# *_*coding:utf-8 *_*
import uvicorn
from fastapi import FastAPI
from configs import FASTAPI_TITLE, FASTAPI_HOST, FASTAPI_PORT

app = FastAPI(title=FASTAPI_TITLE, docs_url=None, redoc_url=None)

if __name__ == '__main__':
    config = uvicorn.Config(app=app, host=FASTAPI_HOST, port=FASTAPI_PORT, workers=1)
    server = uvicorn.Server(config)
    import mylogger
    from info import app_registry

    app_registry(app)
    server.run()
