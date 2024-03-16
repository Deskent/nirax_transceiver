from fastapi.testclient import TestClient
from httpx import AsyncClient
from src.schemas.actions import Action


URL: str = '/ws/json'


async def test_connect_send_echo(
    websocket_client: TestClient,
    atclient: AsyncClient,
):
    client_id: str = 'nirax_websocket_id'
    with websocket_client.websocket_connect(f'{URL}/{client_id}') as websocket:
        payload = {
            'action': Action.echo.value,
        }
        websocket.send_json(payload)
        data = websocket.receive_json()
        assert data == {"action": "echo", "payload": {}}
