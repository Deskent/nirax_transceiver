import datetime
import sys
from pathlib import Path

from loguru import logger
from pydantic import BaseSettings


class Settings(BaseSettings):
    DOCS_URL: str = '/docs'
    DEBUG: bool = False
    BASE_DIR: Path = None
    LOGS_DIR: Path = None
    SERVER_PORT: int = 8100
    TELEBOT_TOKEN: str = ''
    CHAT_ID: int = -943224873
    STAGE: str = ""
    LOGGER_LEVEL: str = "INFO"
    DEFAULT_TIMEOUT: int = 60
    SECRET_HEADER: str = 'nirax_websocket_id'

    class Config:
        env_file = '/.env'


# Main config
BASE_DIR = Path(__file__).parent

env_file = BASE_DIR / '.env'
settings = Settings(_env_file=env_file, _env_file_encoding='utf-8')

settings.BASE_DIR = BASE_DIR

# Logger
if not settings.LOGS_DIR:
    current_date = str(datetime.datetime.today().date())
    settings.LOGS_DIR = BASE_DIR / 'logs' / current_date

log_level = settings.LOGGER_LEVEL
logger.remove()
logger.add(level=log_level, sink=sys.stdout)
logger.add(level=30, sink=settings.LOGS_DIR / 'errors.log', rotation='100 MB')
# logger.add(level=log_level, sink=settings.LOGS_DIR / 'nirax_transceiver.log', rotation='50 MB')
