import asyncio
import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from main import app
from src.enums.enums import RequestTypes
from tests.conftest import URL_TEST


@pytest.fixture(scope='session')
def carreta_api_key() -> str:
    password: str = os.getenv('CARETTA_API_KEY')
    if not password:
        raise ValueError('Env error: CARETTA_API_KEY not found')
    return password


@pytest.fixture
def payload_data(carreta_api_key) -> dict[str, str | dict]:
    return {
        # 'api_key': carreta_api_key,
        # 'q': '4477'
    }


@pytest.fixture
def payload_aiohttp(payload_data) -> dict[str, str | dict]:
    return {
        "supplier": "carreta.ru",
        "request_data": {
            "method": "GET",
            "url": URL_TEST,
            "headers": {},
            "data": payload_data,
            "timeout": 25,
        },
        "request_type": RequestTypes.aiohttp.value,
    }


@pytest.fixture
def payload_requests(payload_data) -> dict[str, str | dict]:
    return {
        "supplier": "carreta.ru",
        "request_data": {
            "method": "GET",
            "url": URL_TEST,
            "headers": {},
            "data": payload_data,
            "timeout": 25,
        },
        "request_type": RequestTypes.requests.value,
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


@pytest.fixture(scope='session')
def base_url() -> str:
    return "/api/transceiver"


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture(scope='session')
async def testclient(base_url: str) -> Generator[TestClient, None, None]:
    yield TestClient(app)


@pytest.fixture
def tclient(testclient: TestClient) -> TestClient:
    with testclient as session:
        yield session
