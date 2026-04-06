from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging
from app.bootstrap.middleware import register_middleware
from app.bootstrap.routes import register_routes


def create_application() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    register_middleware(app, settings)
    register_routes(app)

    return app
