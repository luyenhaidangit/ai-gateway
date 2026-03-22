from decimal import Decimal

from app.repositories.securities_repository import SecuritiesRepository
from app.schemas.securities_schema import SecuritiesAdviceResponse


class SecuritiesService:
    """Business logic for securities investment advice."""

    def __init__(self, repo: SecuritiesRepository):
        self.repo = repo

    async def get_advice(self, symbol: str) -> SecuritiesAdviceResponse | None:
        record = await self.repo.get_latest_by_symbol(symbol)
        if record is None:
            return None

        change_percent = float(record.change_percent or Decimal("0"))
        recommendation = self._get_recommendation(change_percent)
        confidence = self._get_confidence(change_percent, recommendation)

        return SecuritiesAdviceResponse(
            symbol=record.symbol,
            recommendation=recommendation,
            confidence=confidence,
        )

    def _get_recommendation(self, change_percent: float) -> str:
        if change_percent > 0:
            return "BUY"
        if change_percent < 0:
            return "SELL"
        return "HOLD"

    def _get_confidence(self, change_percent: float, recommendation: str) -> float:
        if recommendation == "HOLD":
            return 0.6

        normalized = min(abs(change_percent), 1.0)
        return round(min(0.7 + normalized * 0.4, 0.95), 2)
