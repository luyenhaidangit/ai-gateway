from datetime import datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response body for GET /health."""

    status: str = Field(examples=["healthy", "initializing"])
    database: str = Field(examples=["connected"])
    model_loaded: bool = Field(description="Whether the ML model is fully loaded in RAM")
    timestamp: datetime
