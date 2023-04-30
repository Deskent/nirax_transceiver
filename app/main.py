import os
import platform
import time
import warnings

import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from config import settings, logger
from routers import main_router

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

if platform.system().lower() == "linux":
    os.environ['TZ'] = 'UTC'
    time.tzset()

description = f"""
    Описание работы с API.
"""
APP_DESCRIPTION: dict = {

    "title": "Nirax Transceiver",
    "description": description,
    "version": "2.0",
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

    @app.on_event("startup")
    async def on_startup():
        pass

    @app.middleware("http")
    async def request_logger(request: Request, call_next):
        t0 = time.time()
        response = await call_next(request)
        delta = round((time.time() - t0), 2)
        logger.debug(f'Request [{request.url.path}] returns result after {delta} seconds.')

        return response

    return app


app: FastAPI = get_application()

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=settings.SERVER_PORT, reload=True)
