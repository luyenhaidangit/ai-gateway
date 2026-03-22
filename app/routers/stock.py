from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories.securities_info_repository import SecuritiesInfoRepository
from app.schemas import ErrorDetail, StockAdviceResponse
from app.services.stock_advice_service import StockAdviceService

router = APIRouter(prefix="/stock", tags=["Stock Advice"])


@router.get(
    "/advice/{symbol}",
    response_model=StockAdviceResponse,
    summary="Get investment advice for a stock symbol",
    responses={404: {"model": ErrorDetail, "description": "Stock symbol not found"}},
)
async def get_stock_advice(symbol: str, db: AsyncSession = Depends(get_db)):
    service = StockAdviceService(SecuritiesInfoRepository(db))
    advice = await service.get_advice(symbol)

    if advice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock symbol {symbol.upper()} not found",
        )

    return advice
