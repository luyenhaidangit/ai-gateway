from pydantic import BaseModel, Field


class StockAdviceResponse(BaseModel):
    """Response body for GET /stock/advice/{symbol}."""

    symbol: str = Field(description="Stock symbol")
    recommendation: str = Field(description="Investment recommendation such as BUY, HOLD, or SELL")
    confidence: float = Field(description="Recommendation confidence score from 0.0 to 1.0")
