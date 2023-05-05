from pydantic import BaseModel


class RequestData(BaseModel):
    """Transceiver payload data

    Attributes:

        method: str

        url: str

        params: dict = {}

        headers: dict = {}

        data: dict = {}

        timeout: int = 25
    """

    method: str
    url: str
    params: dict = {}
    headers: dict = {}
    data: dict = {}
    timeout: int = 25


class InputSchema(BaseModel):
    """
    Transceiver input data

    Attributes:
        method: str

        url: str

        params: dict = {}

        headers: dict = {}

        data: dict = {}

        timeout: int = 25

        supplier: str

        request_data: RequestData

        request_type: str = 'aiohttp'
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
