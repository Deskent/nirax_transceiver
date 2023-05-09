import json
from typing import Type

import aiohttp
import aiohttp.client_exceptions
import requests

from config import logger, settings
from src.enums.enums import RequestTypes
from src.exc.exceptions import DataRequestError
from src.schemas.schemas import InputSchema, OutputSchema
from src.types.common import JSON
from src.utils.info_bot import bot


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


class SyncRequester(BaseRequester):

    def _get_response(self) -> requests.Response:
        """Принимает следующие ключи:
            method: str - HTTP-метод, GET, POST, DELETE, PUT, PATCH, etc

            url: str - URL куда отправлять запрос

            params: dict - Query params

            headers: dict - Заголовки запроса

            data: dict - Тело запроса

            timeout: int - Таймаут ожидания ответа

        :return: Возвращает Response
        """

        return requests.request(**self.payload)

    def _get_request_json(self) -> JSON:
        try:
            response: requests.Response = self._get_response()
            status: int = response.status_code
            try:
                data: JSON = response.json()

                return data
            except json.decoder.JSONDecodeError as err:
                logger.error(
                    f'SyncRequester._get_request_json JSON error: {err}'
                    f'\nResponse text: {response.text}'
                    f'\nPayload: {self.payload}'
                )
                raise DataRequestError(
                    f'Ошибка {status} запроса запроса на адрес: {self.payload["url"]}'
                )
        except requests.exceptions.ReadTimeout as err:
            logger.error(
                f'SyncRequester._get_request_json ReadTimeout error: {err}'
                f'\nPayload: {self.payload}'
            )
            raise DataRequestError(
                f'Timeout error: {self.timeout}'
            )
        except requests.exceptions.MissingSchema as err:
            logger.exception(err)
            raise DataRequestError(
                f'Invalid url: {self.payload["url"]}'
            )

    async def send_request(self):
        return self._get_request_json()


class AsyncRequester(BaseRequester):

    async def _get_async_request_json(self) -> JSON:
        """Принимает следующие ключи:
            method: str - HTTP-метод, GET, POST, DELETE, PUT, PATCH, etc

            url: str - URL куда отправлять запрос

            params: dict - Query params

            headers: dict - Заголовки запроса

            data: dict - Тело запроса

            timeout: int - Таймаут ожидания ответа

        :return: Возвращает JSON объект ответа.
        """

        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(**self.payload, ssl=False) as response:
                    status: int = response.status
                    return await response.json()
        except aiohttp.client_exceptions.ContentTypeError as err:
            logger.exception(err)
            raise DataRequestError(
                f'Ошибка {status} запроса запроса на адрес: {self.payload["url"]}'
            )
        except aiohttp.client_exceptions.InvalidURL as err:
            logger.exception(err)
            raise DataRequestError(
                f'Invalid url: {self.payload["url"]}'
            )

    async def send_request(self):
        return await self._get_async_request_json()


class RequestSession(BaseRequester):

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


class MainRequester:
    def __init__(self, data: InputSchema):
        self.data: InputSchema = data
        self.output_data: OutputSchema = OutputSchema()

    async def run_request(self):
        payload: dict = self.data.request_data.dict()
        requests_types: dict = {
            RequestTypes.aiohttp.value: AsyncRequester,
            RequestTypes.requests.value: SyncRequester,
            RequestTypes.session.value: RequestSession,
        }
        worker: Type[BaseRequester] = requests_types[self.data.request_type]
        try:
            self.output_data.data = await worker(payload).send_request()
            self.output_data.result = True
        except DataRequestError as err:
            logger.exception(err)
            self.output_data.message = f'{err}'
        except Exception as err:
            logger.exception(err)
            bot.send_message(
                f'\nMain requester get Error:'
                f'\nSupplier: {self.data.supplier}'
                f'\nURL: {self.data.request_data.url}'
                f'\nError Type: {err.__class__.__name__}'
            )
            bot.send_message(f'Main requester get Error Text: {str(err)}')
            self.output_data.message = f'{err}'

        return self.output_data
