from fastapi import APIRouter

from src.views.api_transceiver import router as transceiver_router

main_router = APIRouter(prefix="/api")
main_router.include_router(transceiver_router)
