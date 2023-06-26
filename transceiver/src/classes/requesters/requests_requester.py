import asyncio
import json

import requests
from loguru import logger

from src.classes.requesters.base_requester import BaseRequester
from src.exc import DataRequestError
from src.types.common import JSON


class RequestsRequester(BaseRequester):
    """Класс для запросов с помощью библиотеки requests"""

    def _get_request_json(self) -> tuple[int, JSON]:
        """Отправляет запрос с заданными параметрами.
        Возвращает кортеж статуса и данных"""

        self.payload.update(verify=self.ssl_verify)
        response: requests.Response = requests.request(**self.payload)
        status: int = response.status_code
        data: JSON = response.json()

        return status, data

    async def _get_request_json_data(self) -> tuple[int, JSON]:
        """Run sync request in async thread"""

        return await asyncio.to_thread(self._get_request_json)

    async def send_request(self) -> JSON:
        """Возвращает результат запроса и обрабатывает ошибки"""

        status: int = 0
        try:
            status, data = await self._get_request_json_data()
            return data

        except requests.exceptions.ChunkedEncodingError as err:
            logger.exception(err)
            self.payload.update(stream=True)
            try:
                status, data = await self._get_request_json_data()
                return data
            except Exception as err:
                logger.error(f'Error with stream: {err}')
                raise DataRequestError('Ошибка запроса к поставщику: Stream')

        except json.decoder.JSONDecodeError as err:
            logger.error(
                f'\n{self.__class__.__name__} error type: {err.__class__.__name__}:'
                f'\nPayload: {self.payload}'
            )
            raise DataRequestError(
                f'Ошибка {status} декодирования запроса на адрес: {self.payload["url"]}'
            )

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
            logger.exception(err)
            logger.error(
                f'\n{self.__class__.__name__} error type: {err.__class__.__name__}:'
                f'\nPayload: {self.payload}'
            )
            raise DataRequestError(
                f'Invalid url: {self.payload["url"]}'
            )
