from fastapi import APIRouter, status

from config import settings, logger
from src.classes.requesters import MainRequester
from src.schemas.schemas import InputSchema, OutputSchema

router = APIRouter(prefix='/transceiver', tags=['Transceiver'], include_in_schema=settings.DEBUG)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=OutputSchema
)
async def check_endpoint():
    """Проверка работы API"""

    answer = OutputSchema(message='OK')
    return answer


@router.get(
    "/healthcheck",
    status_code=status.HTTP_200_OK,
    include_in_schema=settings.DEBUG
)
async def healthcheck():
    logger.debug(f"Checked")
    return 0



@router.post(
    "/resend",
    status_code=status.HTTP_200_OK,
    response_model=OutputSchema
)
async def resend(data: InputSchema):
    return await MainRequester(data).run_request()
