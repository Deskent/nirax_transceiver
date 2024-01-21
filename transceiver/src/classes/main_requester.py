import asyncio
from typing import Type

import aiohttp.client_exceptions
import requests

from config import logger
from src.classes.requesters.aiohttp_requester import AsyncRequester
from src.classes.requesters.base_requester import BaseRequester
from src.classes.requesters.requests_requester import RequestsRequester
from src.classes.requesters.requests_session import RequestSession
from src.classes.requesters.requests_soap import RequestsSoap
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
            RequestTypes.soap.value: RequestsSoap,
        }
        worker: Type[BaseRequester] = requests_types[self.data.request_type]
        try:
            answer: dict | list | str = await worker(
                payload=payload,
                ssl_verify=self.data.ssl_verify,
                create_form_data=self.data.create_form_data
            ).send_request()
            if self.data.request_type != RequestTypes.soap.value:
                if isinstance(answer, dict) and (status := answer.get('status_code')):
                    self.output_data.status_code = status
                    self.output_data.text = answer.get('text', '')
                    self.output_data.message = (
                        f'Ошибка запроса к поставщику {self.data.supplier}: Статус: {status}'
                    )

                    return self.output_data
                elif isinstance(answer, str):
                    self.output_data.data = {"transceiver_result": answer}
                else:
                    self.output_data.data = answer if answer is not None else {}

            self.output_data.result = True

            return self.output_data

        except DataRequestError as err:
            logger.error(err)
            self.output_data.message = f'{err}'

        except (
                asyncio.exceptions.TimeoutError,
                aiohttp.client_exceptions.ClientPayloadError
        ) as err:
            logger.error(err)
            self.output_data.message = f'Ошибка запроса к поставщику: Ошибка таймаута {self.timeout}'

        except requests.exceptions.ConnectionError as err:
            logger.error(err)
            self.output_data.message = 'Ошибка запроса к поставщику: Ошибка подключения'

        except (
                aiohttp.client_exceptions.ClientConnectorError,
                aiohttp.client_exceptions.ServerDisconnectedError,
        )as err:
            logger.error(err)
            self.output_data.message = 'Ошибка запроса к поставщику: слишком много запросов в данный момент'

        except Exception as err:
            logger.exception(err)
            bot.send_message(f'Main requester get Error Text: {str(err)}')
            bot.send_message(
                f'\nMain requester get error type: {err.__class__.__name__}'
                f'\nSupplier: {self.supplier}'
                f'\nRequested data: {self.data.request_data.dict()}'
                f'\nURL: {self.data.request_data.url}'
            )
            self.output_data.message = 'Ошибка запроса к поставщику'

        self.output_data.errors.append({self.supplier: self.data.request_data})
        return self.output_data
