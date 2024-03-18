from typing import Annotated

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from config import logger
from .manager import ConnectionManager, get_ws_manager
from ..schemas.actions import Action

router = APIRouter(prefix='/ws', tags=['Websocket'])


@router.get('/info')
async def info():
    return {'version': ''}


@router.get('/actions')
async def get_all_actions():
    return Action.values()


@router.websocket("/json/{client_id}")
async def websocket_json_endpoint(
    websocket: WebSocket,
    client_id: str,
    manager: Annotated[ConnectionManager, Depends(get_ws_manager)],
):
    logger.debug(f"Client ID: {client_id}. Websocket {websocket}")
    try:
        await manager.connect(websocket, client_id)

        while True:
            try:
                await manager.handle_json(websocket)
            except WebSocketDisconnect:
                raise
            except Exception as err:
                logger.exception(err)
                raise WebSocketDisconnect

    except WebSocketDisconnect:
        await manager.disconnect(websocket)

    except Exception as err:
        logger.exception(err)
        await manager.disconnect(websocket)
