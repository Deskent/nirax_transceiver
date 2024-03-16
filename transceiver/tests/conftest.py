from config import env_file
from dotenv import load_dotenv

load_dotenv(env_file)

URL_TEST: str = "http://jsonplaceholder.typicode.com/posts"
# URL_TEST: str = "http://api.carreta.ru/v1/search"

pytest_plugins = [
    'tests.fixtures.app_fixtures',
]
