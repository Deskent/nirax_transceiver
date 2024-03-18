from fastapi import APIRouter, status

from config import settings
from src.classes.main_requester import handle_request
from src.schemas.schemas import InputSchema, OutputSchema

router = APIRouter(prefix='/transceiver', tags=['Transceiver'], include_in_schema=settings.DEBUG)


@router.post(
    "/resend",
    status_code=status.HTTP_200_OK,
    response_model=OutputSchema,
)
async def resend(data: InputSchema):
    return await handle_request(data)
