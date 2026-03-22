from datetime import datetime

from pydantic import BaseModel, Field


class InferenceRequest(BaseModel):
    """Request body for POST /api/infer."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The text to classify",
        examples=["This new feature is absolutely amazing, I love it!"],
    )


class InferenceResponse(BaseModel):
    """Response body for inference endpoints."""

    id: int
    text: str = Field(description="The original text input")
    prediction: str = Field(description="Classification result (Positive/Negative/Neutral)")
    confidence: float = Field(description="Model confidence score (0.0 to 1.0)")
    model_version: str = Field(description="The model version used for inference")
    created_at: datetime

    class Config:
        from_attributes = True


class ErrorDetail(BaseModel):
    """Standard error response."""

    detail: str
