from pydantic import BaseModel


class ServiceInfoResponse(BaseModel):
    """Response body for GET /."""

    service: str
    status: str
    version: str
    docs: str
    health: str
