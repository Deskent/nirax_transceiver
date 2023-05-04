from fastapi import APIRouter, status

from config import settings, logger
from src.classes.requesters import MainRequester
from src.schemas.schemas import InputSchema, OutputSchema

router = APIRouter(prefix='/transceiver', tags=['Transceiver'], include_in_schema=settings.DEBUG)


@router.post(
    "/resend",
    status_code=status.HTTP_200_OK,
    response_model=OutputSchema
)
async def resend(data: InputSchema):
    logger.debug(data)
    results = await MainRequester(data).run_request()
    logger.debug(results)
    return results
