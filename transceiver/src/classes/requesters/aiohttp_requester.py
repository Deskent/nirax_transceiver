import json

import aiohttp
import aiohttp.client_exceptions
from loguru import logger

from src.classes.requesters.base_requester import BaseRequester
from src.exc import DataRequestError
from src.types.common import JSON
from src.utils.info_bot import bot


class AsyncRequester(BaseRequester):
    """Class realize request using aiohttp library"""

    async def _create_form_data(self, data: dict) -> aiohttp.FormData:
        """Создает FormData для некоторых поставщиков, например для PARTKOM"""

        form_data = aiohttp.FormData()
        for key, value in data.items():
            if isinstance(value, (str, int, float, bool)):
                form_data.add_field(key, value)
            elif isinstance(value, list):
                for index, order_item in enumerate(value):
                    for item_name, item_value in order_item.items():
                        form_data.add_field(f"{key}[{index}][{item_name}]", item_value)

        return form_data

    async def update_payload_with_form_data(self):
        """Update payload data as FormData"""

        data: dict = self.payload.get('data')
        if not isinstance(data, dict):
            raise DataRequestError(f'Payload data must be dict, got {type(data)}')
        form_data: aiohttp.FormData = await self._create_form_data(self.payload['data'])
        self.payload.update(data=form_data)

    async def update_payload_with_ssl(self):
        """Add SSL param to payload"""

        ssl: bool = self.ssl_verify if self.ssl_verify is not None else False
        self.payload.update(ssl=ssl)

    async def _get_async_request_json(self) -> JSON:
        """self.payload: dict = {

            method: str - HTTP-метод, GET, POST, DELETE, PUT, PATCH, etc

            url: str - URL куда отправлять запрос

            params: dict - Query params

            headers: dict - Заголовки запроса

            data: dict - Тело запроса

            timeout: int - Таймаут ожидания ответа
        }
        :return: Возвращает JSON объект ответа.
        """

        if self.create_form_data:
            await self.update_payload_with_form_data()
        await self.update_payload_with_ssl()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(**self.payload) as response:
                    status: int = response.status
                    answer_text: str = await response.text()
                    if status == 204:
                        return {}
                    elif status in range(200, 300):
                        if response.content_type == 'application/json':
                            data: JSON = await response.json()
                        else:
                            text: str = await response.text()
                            data: JSON = json.loads(text)
                        return data
                    return {
                        'status_code': status,
                        'text': answer_text
                    }

        except aiohttp.client_exceptions.ContentTypeError as err:
            text: str = (
                f'\n{self.__class__.__name__} error type: {err.__class__.__name__}:'
                f'\n{status=}'
                f'\n{self.payload=}'
                f'\n{answer_text=}'
                f'\n{err=}'
            )
            logger.error(text)

            try:
                answer_text_json: dict = json.loads(answer_text)
                error_text: str = answer_text_json.get('errors', {}).get('FaultDetail', f'{err.__class__.__name__}')
                logger.error(f'{error_text=}')
            except Exception:
                bot.send_message(f'ContentTypeError:'
                                 f'\n{self.payload=}'
                                 f'\n{text=}')
                bot.send_message(f'{answer_text=}')
                error_text: str = f'Тип ошибки: {err.__class__.__name__}'

                if status:
                    error_text += f' Статус: {status}'

            raise DataRequestError(f'Ошибка ответа сервера поставщика: {error_text}')

        except aiohttp.ClientOSError as err:
            logger.error(err)
            raise DataRequestError(
                f'Ошибка ответа сервера поставщика: Тип ошибки: {err.__class__.__name__}'
            )

        except aiohttp.client_exceptions.InvalidURL as err:
            logger.error(err)
            logger.error(
                f'\n{self.__class__.__name__} error type: {err.__class__.__name__}:'
                f'\nPayload: {self.payload}'
            )
            raise DataRequestError(f'Invalid url: {self.payload["url"]}')

    async def send_request(self):
        return await self._get_async_request_json()
