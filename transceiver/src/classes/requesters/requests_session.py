import asyncio

import requests
from loguru import logger

from src.classes.requesters.base_requester import BaseRequester
from src.exc import DataRequestError
from src.types.common import JSON
from src.utils.info_bot import bot


class RequestSession(BaseRequester):
    """Class realize requests with session"""

    def _get_request_json(self) -> dict:

        session = requests.session()
        session.headers = self.payload['headers']
        verify: bool = self.ssl_verify if self.ssl_verify is not None else False
        try:
            response = session.request(
                method=self.payload['method'],
                url=self.payload['url'],
                data=self.payload['data'].encode('utf-8'),
                verify=verify,
            )
            return {'status': response.status_code, 'content': response.content}

        except Exception as err:
            logger.exception(err)
            error_text: str = (
                f'\n{self.__class__.__name__} error type: {err.__class__.__name__}:'
                f'\nPayload: {self.payload}'
            )
            logger.error(error_text)
            bot.send_message(error_text)

            raise DataRequestError(
                f'Error {err.__class__.__name__} {self.payload["url"]}'
            )

    async def _get_request_json_data(self) -> JSON:
        """Run sync request in async thread"""

        return await asyncio.to_thread(self._get_request_json)

    async def send_request(self) -> dict:
        return await self._get_request_json_data()
