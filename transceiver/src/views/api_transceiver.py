import asyncio

from fastapi import APIRouter, status

from config import settings, logger
from src.classes.main_requester import MainRequester
from src.schemas.schemas import InputSchema, OutputSchema

router = APIRouter(prefix='/transceiver', tags=['Transceiver'], include_in_schema=settings.DEBUG)


@router.post(
    "/resend",
    status_code=status.HTTP_200_OK,
    response_model=OutputSchema
)
async def resend(data: InputSchema):
    logger.info(data)
    try:
        results = await MainRequester(data).run_request()
        logger.info(results)
        return results
    except asyncio.exceptions.TimeoutError as err:
        logger.error(err)
        return OutputSchema(
            message=f'Ошибка запроса к поставщику: Ошибка таймаута: {data.request_data.timeout}'
        )

    except Exception as err:
        logger.exception(err)
    return OutputSchema(message='Ошибка запроса к поставщику: общая')
