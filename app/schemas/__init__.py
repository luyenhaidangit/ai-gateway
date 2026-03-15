# app/schemas/__init__.py

from app.schemas.inference_schema import (
    ErrorDetail,
    HealthResponse,
    InferenceRequest,
    InferenceResponse,
)

__all__ = ["InferenceRequest", "InferenceResponse", "HealthResponse", "ErrorDetail"]
