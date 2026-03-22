from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import HealthResponse
from app.services.health_service import check_database_health

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Service health check",
    description="Check database connectivity.",
)
async def health_check(db: AsyncSession = Depends(get_db)):
    db_healthy = await check_database_health(db)
    system_status = "healthy" if db_healthy else "degraded"

    return HealthResponse(
        status=system_status,
        database="connected" if db_healthy else "disconnected",
        timestamp=datetime.now(timezone.utc),
    )
