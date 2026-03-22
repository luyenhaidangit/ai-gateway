from fastapi import FastAPI

from app.routers.api import router as api_router
from app.routers.health import router as health_router
from app.routers.stock import router as stock_router


def register_routes(app: FastAPI) -> None:
    app.include_router(api_router)
    app.include_router(health_router)
    app.include_router(stock_router)
