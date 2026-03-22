from datetime import datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response body for GET /health."""

    status: str = Field(examples=["healthy", "degraded"])
    database: str = Field(examples=["connected"])
    timestamp: datetime
