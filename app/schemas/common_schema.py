from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Standard error response."""

    detail: str
