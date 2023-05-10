import asyncio
from typing import Type

import requests

from config import logger
from src.classes.requesters.aiohttp_requester import AsyncRequester
from src.classes.requesters.base_requester import BaseRequester
from src.classes.requesters.requests_requester import RequestsRequester
from src.classes.requesters.requests_session import RequestSession
from src.enums.enums import RequestTypes
from src.exc.exceptions import DataRequestError
from src.schemas.schemas import InputSchema, OutputSchema
from src.utils.info_bot import bot


class MainRequester:
    """Dispatcher for requesters"""

    def __init__(self, data: InputSchema):
        self.data: InputSchema = data
        self.output_data: OutputSchema = OutputSchema()
        self.timeout: int = self.data.request_data.timeout
        self.supplier: str = self.data.supplier

    async def run_request(self):
        payload: dict = self.data.request_data.dict()
        requests_types: dict = {
            RequestTypes.aiohttp.value: AsyncRequester,
            RequestTypes.requests.value: RequestsRequester,
            RequestTypes.session.value: RequestSession,
        }
        worker: Type[BaseRequester] = requests_types[self.data.request_type]
        try:
            self.output_data.data = await worker(payload).send_request()
            self.output_data.result = True

        except DataRequestError as err:
            logger.exception(err)
            self.output_data.message = f'{err}'

        except asyncio.exceptions.TimeoutError as err:
            logger.exception(err)
            self.output_data.message = f'Ошибка запроса к поставщику: Ошибка таймаута {self.timeout}'

        except requests.exceptions.ConnectionError as err:
            logger.exception(err)
            self.output_data.message = 'Ошибка запроса к поставщику: Ошибка подключения'

        except Exception as err:
            logger.exception(err)
            bot.send_message(
                f'\nMain requester get Error:'
                f'\nSupplier: {self.supplier}'
                f'\nURL: {self.data.request_data.url}'
                f'\nError Type: {err.__class__.__name__}'
            )
            bot.send_message(f'Main requester get Error Text: {str(err)}')
            self.output_data.message = 'Ошибка запроса к поставщику'

        return self.output_data
