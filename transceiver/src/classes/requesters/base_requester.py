from config import settings


class BaseRequester:
    """
    Base class for HTTP requests.

        Attributes:
            payload - Request params for sending

            ssl_verify - SSL request param

            timeout - Maximum request timeout

            create_form_data - If True - will be created aiohttp.FormData before request
                (Only for AsyncRequester class)
        Methods
            send_request
    """

    def __init__(self, payload: dict, ssl_verify: bool = None, create_form_data: bool = False):
        self.payload: dict = payload
        self.ssl_verify: bool = ssl_verify
        self.timeout: int = self.payload.get('timeout', settings.DEFAULT_TIMEOUT)
        self.create_form_data: bool = create_form_data

    async def send_request(self):
        raise NotImplementedError
