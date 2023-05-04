from pydantic import BaseModel


class RequestData(BaseModel):
    method: str
    url: str
    headers: dict
    data: dict = {}
    timeout: int = 25


class InputSchema(BaseModel):
    """
    Attributes:

    """

    supplier: str
    request_data: RequestData
    request_type: str = 'aiohttp'


class OutputSchema(BaseModel):
    """
    Attributes:
        result: bool = False

        total: int = 0

        message: str = ''

        errors: list = []

        data: list = []
    """

    result: bool = False
    total: int = 0
    message: str = ''
    errors: list = []
    data: list | dict = {}
