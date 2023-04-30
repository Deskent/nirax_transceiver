from fastapi import APIRouter, status

from config import settings
from src.classes.requesters import MainRequester
from src.schemas.schemas import InputSchema, OutputSchema

include: bool = settings.DEBUG
router = APIRouter(prefix='/transceiver', tags=['Transceiver'], include_in_schema=include)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=OutputSchema
)
async def check_endpoint():
    """Проверка работы API"""

    answer = OutputSchema(message='OK')
    return answer


@router.post(
    "/aiohttp",
    status_code=status.HTTP_200_OK,
    response_model=OutputSchema
)
async def aiohttp_post(data: InputSchema):
    return await MainRequester(data).run_request()
