from enum import Enum


class RequestTypes(Enum):
    requests = 'requests'
    aiohttp = 'aiohttp'
    session = 'session'
