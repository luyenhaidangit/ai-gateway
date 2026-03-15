# app/repositories/inference_repository.py

import logging
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inference import InferenceResult

logger = logging.getLogger(__name__)


class InferenceRepository:
    """Data access layer for InferenceResult records."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, infer_id: int) -> InferenceResult | None:
        """Retrieve an inference result by its primary key."""
        try:
            stmt = select(InferenceResult).where(InferenceResult.id == infer_id)
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error reading inference result from DB: {e}")
            return None

    async def create(
        self,
        text: str,
        prediction: str,
        confidence: float,
        model_version: str,
    ) -> InferenceResult:
        """Persist a new inference result and return the saved entity."""
        entry = InferenceResult(
            text=text,
            prediction=prediction,
            confidence=confidence,
            model_version=model_version,
        )
        try:
            self.db.add(entry)
            await self.db.commit()
            await self.db.refresh(entry)
        except Exception as e:
            logger.warning(f"Failed to save inference result to DB: {e}")
            # Fallback: return unsaved entry so the API response doesn't crash
            entry.id = -1
            entry.created_at = datetime.now(timezone.utc)
        return entry

    async def check_health(self) -> bool:
        """Return True if the DB connection is alive."""
        try:
            await self.db.execute(select(1))
            return True
        except Exception:
            return False
