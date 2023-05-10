import requests
from loguru import logger

from src.classes.requesters.base_requester import BaseRequester


class RequestSession(BaseRequester):
    """Class realize requests with session"""

    def _get_request_json(self) -> dict:

        session = requests.session()
        session.headers = self.payload['headers']

        response = session.request(
            method=self.payload['method'],
            url=self.payload['url'],
            data=self.payload['data'].encode('utf-8'),
            verify=False,
        )
        logger.debug((response.status_code, response.content))
        return {'status': response.status_code, 'content': response.content}

    async def send_request(self) -> dict:
        return self._get_request_json()
