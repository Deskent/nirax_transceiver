from fastapi import FastAPI

from .manager import ConnectionManager, get_ws_manager
from .router import router


def _update_dependencies(app: FastAPI):
    app.dependency_overrides[ConnectionManager] = get_ws_manager


def connect_ws(app):
    _update_dependencies(app)
    app.include_router(router)
