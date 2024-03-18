from fastapi.testclient import TestClient

from config import settings
from src.schemas.actions import Action


URL: str = '/ws/json'


async def test_get_all_actions(tclient: TestClient):
    response = tclient.get('/ws/actions')
    assert response.status_code == 200
    assert response.json() == Action.values()


async def test_connect_execute_correct(
    testclient: TestClient,
    payload_requests: dict,
):
    client_id: str = settings.SECRET_HEADER
    with testclient.websocket_connect(f'{URL}/{client_id}') as websocket:
        payload: dict = {
            'action': Action.execute.value,
            'payload': payload_requests,
        }
        websocket.send_json(payload)
        data: dict = websocket.receive_json()
        assert data['message'] == ''
        assert data['errors'] == []
        assert data['data']
        assert data['result']


async def test_connect_execute_bad_url(
    testclient: TestClient,
    payload_requests: dict,
):
    client_id: str = settings.SECRET_HEADER
    with testclient.websocket_connect(f'{URL}/{client_id}') as websocket:
        payload_requests['request_data']['url'] = 'wrong_url'
        payload: dict = {
            'action': Action.execute.value,
            'payload': payload_requests,
        }
        websocket.send_json(payload)
        data: dict = websocket.receive_json()
        assert data['message'].startswith('Invalid url')
        assert data['errors'] != []
        assert data['result'] is False
