from config import settings


class BaseRequester:
    """Base class for HTTP requests

        Attributes:

            DEFAULT_TIMEOUT: int = 25 - Class attribute - Maximum request timeout
    """

    def __init__(self, payload: dict):
        self.payload: dict = payload
        self.timeout: int = self.payload.get('timeout', settings.DEFAULT_TIMEOUT)

    async def send_request(self):
        raise NotImplementedError
