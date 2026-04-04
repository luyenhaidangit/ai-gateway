from fastapi import APIRouter

from app.core.dependencies import SettingsDep
from app.schemas import ServiceInfoResponse

router = APIRouter(tags=["Service"])


@router.get(
    "/",
    response_model=ServiceInfoResponse,
    summary="Service information",
    description="Return basic service metadata and useful entry points.",
)
async def service_info(settings: SettingsDep) -> ServiceInfoResponse:
    service_name = "-".join(settings.APP_TITLE.strip().split()).lower()

    return ServiceInfoResponse(
        service=service_name,
        status="running",
        version=settings.APP_VERSION,
        docs="/docs",
        health="/health",
    )
