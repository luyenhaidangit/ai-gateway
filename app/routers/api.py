from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.schemas import InferenceRequest, InferenceResponse, HealthResponse, ErrorDetail
from app.services.core import (
    ml_model,
    get_inference_by_id,
    save_inference_result,
    check_database_health,
)

router = APIRouter(prefix="/api", tags=["MLOps Inference Server"])


@router.post(
    "/infer",
    response_model=InferenceResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit text for classification inference",
    description=(
        "Send raw text to the currently loaded ML model. "
        "The model predicts the sentiment (Positive/Negative/Neutral) "
        "and returns a confidence score. Results are logged to the database."
    ),
    responses={
        422: {"model": ErrorDetail, "description": "Validation error"},
        503: {"model": ErrorDetail, "description": "Model not loaded yet"},
    },
)
async def infer(request: InferenceRequest, db: AsyncSession = Depends(get_db)):
    if not ml_model.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML Model is currently initializing and not ready to accept requests.",
        )
        
    # Run Inference (sync, blocking operation simulated)
    # In a real MLOps server, this would run in a separate ThreadPool if CPU intensive
    result = ml_model.predict(request.text)

    # Save to DB history
    entry = await save_inference_result(
        text=request.text,
        prediction=result["prediction"],
        confidence=result["confidence"],
        model_version=ml_model.version,
        db=db,
    )

    return InferenceResponse(
        id=entry.id,
        text=entry.text,
        prediction=entry.prediction,
        confidence=entry.confidence,
        model_version=entry.model_version,
        created_at=entry.created_at,
    )


@router.get(
    "/infer/{infer_id}",
    response_model=InferenceResponse,
    summary="Get past inference result by ID",
    description="Retrieve a previously executed inference classification from the history database.",
    responses={
        404: {"model": ErrorDetail, "description": "Result not found"},
    },
)
async def get_inference(infer_id: int, db: AsyncSession = Depends(get_db)):
    entry = await get_inference_by_id(infer_id, db)

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inference record with id {infer_id} not found",
        )

    return InferenceResponse(
        id=entry.id,
        text=entry.text,
        prediction=entry.prediction,
        confidence=entry.confidence,
        model_version=entry.model_version,
        created_at=entry.created_at,
    )


# ─── Health Check (outside /api prefix) ──────────────────────

health_router = APIRouter(tags=["Health"])


@health_router.get(
    "/health",
    response_model=HealthResponse,
    summary="Service and Model health check",
    description="Check database connectivity and whether the ML model is fully loaded in RAM.",
)
async def health_check(db: AsyncSession = Depends(get_db)):
    db_healthy = await check_database_health(db)
    model_loaded = ml_model.is_loaded
    
    sys_status = "healthy" if (db_healthy and model_loaded) else "initializing" if not model_loaded else "degraded"

    return HealthResponse(
        status=sys_status,
        database="connected" if db_healthy else "disconnected",
        model_loaded=model_loaded,
        timestamp=datetime.now(timezone.utc),
    )
