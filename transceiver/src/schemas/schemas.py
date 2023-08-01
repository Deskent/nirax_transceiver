from pydantic import BaseModel


class RequestData(BaseModel):
    """Transceiver payload data

    Attributes:

        method: str

        url: str

        params: dict | None = {}

        headers: dict = {}

        data: dict = {}

        timeout: int = 25


    """

    method: str
    url: str
    params: dict | None = {}
    headers: dict = {}
    data: dict | str = {}
    timeout: int = 25


class InputSchema(BaseModel):
    """
    Transceiver input data

    Attributes:

        supplier: str - Поставщик

        request_data: RequestData - Данные для отправки запроса

        request_type: str = 'aiohttp' - Тип запроса

        ssl_verify: bool = None

        create_form_data: bool = False - Transceiver send data as aiohttp.FormData
    """

    supplier: str
    request_data: RequestData
    request_type: str = 'aiohttp'
    ssl_verify: bool = None
    create_form_data: bool = False


class OutputSchema(BaseModel):
    """
    Attributes:
        result: bool = False

        total: int = 0

        message: str = ''

        errors: list = []

        data: list = []

        status_code: int = 0

        text: str = ''
    """

    result: bool = False
    total: int = 0
    message: str = ''
    errors: list = []
    data: list | dict = {}
    status_code: int = 0
    text: str = ''
