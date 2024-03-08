import os
import platform
import time
import warnings

import uvicorn
from fastapi import FastAPI, Request, status
from starlette.middleware.cors import CORSMiddleware

from config import settings, logger
from routers import main_router
from _resources import __appname__, __version__
from src.ws_router import connect_ws

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

if platform.system().lower() == "linux":
    os.environ['TZ'] = 'UTC'
    time.tzset()

description = f"""
    Описание работы с Transceiver.
"""
APP_DESCRIPTION: dict = {

    "title": __appname__,
    "description": description,
    "version": __version__,
    "docs_url": settings.DOCS_URL,
    "redoc_url": settings.DOCS_URL,
    "debug": settings.DEBUG,
    "contact": {
        "url": f"http://suppliers.nirax.ru{settings.DOCS_URL}",
    }
}


def add_cors_middleware(app: FastAPI) -> FastAPI:
    ALLOWED_HOSTS = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


def get_application():
    app = FastAPI(**APP_DESCRIPTION)

    app.include_router(main_router)

    app: FastAPI = add_cors_middleware(app)

    connect_ws(app)

    @app.on_event("startup")
    async def on_startup():
        pass

    @app.get(
        "/healthcheck",
        status_code=status.HTTP_200_OK,
        include_in_schema=settings.DEBUG
    )
    async def healthcheck():
        return __appname__

    return app


app: FastAPI = get_application()

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=settings.SERVER_PORT, reload=True)
