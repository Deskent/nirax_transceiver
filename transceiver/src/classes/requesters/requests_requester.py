import json

import requests
from loguru import logger

from src.classes.requesters.base_requester import BaseRequester
from src.exc import DataRequestError
from src.types.common import JSON


class RequestsRequester(BaseRequester):

    def _get_response(self) -> requests.Response:
        """Принимает следующие ключи:
            method: str - HTTP-метод, GET, POST, DELETE, PUT, PATCH, etc

            url: str - URL куда отправлять запрос

            params: dict - Query params

            headers: dict - Заголовки запроса

            data: dict - Тело запроса

            timeout: int - Таймаут ожидания ответа

            ssl_verify: bool = False

        :return: Возвращает Response
        """
        self.payload.update(verify=self.ssl_verify)
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
                    f'\n{self.__class__.__name__} error type: {err.__class__.__name__}:'
                    f'\n{response.text=}'
                    f'\nPayload: {self.payload}'
                )
                raise DataRequestError(
                    f'Ошибка {status} запроса запроса на адрес: {self.payload["url"]}'
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

    async def send_request(self):
        return self._get_request_json()
