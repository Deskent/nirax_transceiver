import aiohttp
import aiohttp.client_exceptions
from loguru import logger

from src.classes.requesters.base_requester import BaseRequester
from src.exc import DataRequestError
from src.types.common import JSON
from src.utils.info_bot import bot


class AsyncRequester(BaseRequester):
    """Class realize request using aiohttp library"""

    async def _get_async_request_json(self) -> JSON:
        """Принимает следующие ключи:
            method: str - HTTP-метод, GET, POST, DELETE, PUT, PATCH, etc

            url: str - URL куда отправлять запрос

            params: dict - Query params

            headers: dict - Заголовки запроса

            data: dict - Тело запроса

            timeout: int - Таймаут ожидания ответа

            ssl_verify: bool = None

        :return: Возвращает JSON объект ответа.
        """

        ssl: bool = self.ssl_verify if self.ssl_verify is not None else False
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(**self.payload, ssl=ssl) as response:
                    return await response.json()

        except aiohttp.client_exceptions.ContentTypeError as err:
            logger.exception(err)
            text: str = (
                f'\n{self.__class__.__name__} error type: {err.__class__.__name__}:'
                f'\nPayload: {self.payload}'
            )
            logger.error(text)
            bot.send_message(text)
            raise DataRequestError(
                f'Ошибка ответа сервера поставщика: {err.__class__.__name__}'
            )

        except aiohttp.client_exceptions.InvalidURL as err:
            logger.exception(err)
            logger.error(
                f'\n{self.__class__.__name__} error type: {err.__class__.__name__}:'
                f'\nPayload: {self.payload}'
            )
            raise DataRequestError(
                f'Invalid url: {self.payload["url"]}'
            )

    async def send_request(self):
        return await self._get_async_request_json()
