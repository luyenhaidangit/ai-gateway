from fastapi import FastAPI

from app.routers.api import health_router
from app.routers.api import router as api_router


def register_routes(app: FastAPI) -> None:
    app.include_router(api_router)
    app.include_router(health_router)
