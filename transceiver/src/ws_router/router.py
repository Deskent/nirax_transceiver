from typing import Annotated

from config import logger
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from .manager import ConnectionManager
from ..schemas.value_objects import ActionDTO

router = APIRouter(prefix='/ws', tags=['Websocket'])


@router.get('/info')
async def info():
    return {'version': ''}


@router.websocket("/json/{client_id}")
async def websocket_json_endpoint(
    websocket: WebSocket,
    client_id: str,
    manager: Annotated[ConnectionManager, Depends()],
):
    await websocket.accept()
    # await manager.connect(websocket)
    try:
        if client_id != 'nirax_websocket_id':
            raise WebSocketDisconnect

        while True:
            try:
                data: dict = await websocket.receive_json()
                dto = ActionDTO(**data)
                await websocket.send_json(dto.dict())
            except Exception as err:
                logger.exception(err)
                raise WebSocketDisconnect

    except WebSocketDisconnect:
        await websocket.close()

    except Exception as err:
        logger.exception(err)
        await websocket.close()
