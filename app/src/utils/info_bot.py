from typing import Iterable

import requests
from requests import Response

from config import logger, settings


class Bot:
    """Telegram Bot API interface to send messages to certain chats/users"""

    _API_HOST: str = 'api.telegram.org'

    def __init__(self, bot_token: str, chat_id: str, timeout: int = 10, parse_mode: str = 'HTML'):
        self._token: str = bot_token
        self.chat_id: str = chat_id
        self.timeout: int = timeout
        self.parse_mode: str = parse_mode

    def send_message(self, message: str) -> Response:
        """Send message through Telegram bot"""

        headers: dict = {'Content-Type': 'application/json'}
        data: dict = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': self.parse_mode
        }
        logger.debug(f'Sending message via info bot... Data:\n\t{data}')
        return self._send_api_request('sendMessage', headers=headers, json=data)

    def send_document(self, files: Iterable, caption: str | None = None) -> Response:
        """Send file as Telegram document"""

        data: dict = {
            'chat_id': self.chat_id,
            'caption': caption if caption else '',
            'parse_mode': self.parse_mode,
        }
        logger.debug(f'Sending document via info bot... Data:\n\t{data}')
        return self._send_api_request('sendDocument', headers={}, data=data, files=files)

    def _send_api_request(self, api_method: str, headers: dict, *_, **kwargs) -> Response:
        url: str = f'https://{self._API_HOST}/bot{self._token}/{api_method}'
        logger.debug(f'Sending request to Telegram Bot API: {api_method=}, {headers=}, {kwargs=}')
        response: Response = requests.post(url, headers=headers, timeout=self.timeout, **kwargs)
        logger.debug(f'Response from Telegram Bot API: {response.json()}')

        return response


bot: Bot = Bot(bot_token=settings.TELEBOT_TOKEN, chat_id=settings.CHAT_ID)
