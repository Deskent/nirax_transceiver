import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from config import env_file
from main import app
from src.enums.enums import RequestTypes

load_dotenv(env_file)

# URL_TEST: str = "http://jsonplaceholder.typicode.com/posts"
URL_TEST: str = "http://api.carreta.ru/v1/search"


@pytest.fixture(scope='session')
def carreta_api_key() -> str:
    password: str = os.getenv('CARETTA_API_KEY')
    if not password:
        raise ValueError('Env error: CARETTA_API_KEY not found')
    return password


@pytest.fixture
def payload_aiohttp(carreta_api_key) -> dict[str, str | dict]:
    return {
        "supplier": "carreta.ru",
        "request_data": {
            "method": "GET",
            "url": URL_TEST,
            "headers": {},
            "data": {
                'api_key': carreta_api_key,
                'q': '4477'
            },
            "timeout": 25
        },
        "request_type": RequestTypes.aiohttp.value
    }


@pytest.fixture
def payload_requests(carreta_api_key) -> dict[str, str | dict]:
    return {
        "supplier": "carreta.ru",
        "request_data": {
            "method": "GET",
            "url": URL_TEST,
            "headers": {},
            "data": {
                'api_key': carreta_api_key,
                'q': '4477'
            },
            "timeout": 25
        },
        "request_type": RequestTypes.requests.value
    }


@pytest.fixture
def host_prod() -> str:
    host_prod: str = os.getenv('HOST_PROD_URL')
    if not host_prod:
        raise ValueError('Env error: HOST_PROD_URL not found')
    return host_prod


@pytest.fixture
def host_test() -> str:
    host_test: str = os.getenv('HOST_TEST_URL')
    if not host_test:
        raise ValueError('Env error: HOST_TEST_URL not found')
    return host_test


@pytest.fixture
def tclient() -> TestClient:
    client = TestClient(app=app)
    with client as session:
        yield session


@pytest.fixture
def base_url() -> str:
    return "/api/transceiver"
