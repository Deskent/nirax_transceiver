import aiohttp
from loguru import logger

from src.classes.requesters.base_requester import BaseRequester
from src.exc import DataRequestError
from src.types.common import JSON


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
