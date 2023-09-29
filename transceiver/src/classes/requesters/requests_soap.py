import asyncio

import requests
from loguru import logger

from src.classes.requesters.base_requester import BaseRequester
from src.exc import DataRequestError
from src.types.common import JSON


class RequestsSoap(BaseRequester):
    """Класс для запросов с помощью библиотеки requests к сервисам,
    использующим soap"""

    def _get_request_data(self) -> JSON:
        """Отправляет запрос с заданными параметрами.
        Возвращает кортеж статуса и данных"""

        self.payload.update(verify=self.ssl_verify)
        response: requests.Response = requests.request(**self.payload)
        status: int = response.status_code
        if status == 204:
            return {}
        return {
            'status_code': status,
            'text': response.text
        }

    async def _get_request_json_data(self) -> JSON:
        """Run sync request in async thread"""

        return await asyncio.to_thread(self._get_request_data)

    async def send_request(self) -> JSON:
        """Возвращает результат запроса и обрабатывает ошибки"""

        try:
            return await self._get_request_json_data()

        except (
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout,
        ) as err:
            logger.error(
                f'\n{self.__class__.__name__} error type: {err.__class__.__name__}:'
                f'\nPayload: {self.payload}'
            )
            raise DataRequestError(f'Timeout error: {self.timeout}')

        except requests.exceptions.MissingSchema as err:
            logger.error(
                f'\n{self.__class__.__name__} error type: {err.__class__.__name__}:'
                f'\nPayload: {self.payload}'
            )
            raise DataRequestError(
                f'Invalid url: {self.payload["url"]}'
            )
