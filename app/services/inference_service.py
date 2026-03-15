# app/services/inference_service.py

import asyncio
import logging
import random

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.inference import InferenceResult
from app.repositories.inference_repository import InferenceRepository

logger = logging.getLogger(__name__)


# ─── ML Model Singleton ───────────────────────────────────────

class MLModelSingleton:
    """Mock ML Model representing a loaded AI model in memory."""

    _instance = None
    _is_loaded = False
    _model_version = ""

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def load_model(self) -> None:
        """Simulate loading model weights into RAM on startup (~2s)."""
        if not self._is_loaded:
            logger.info("Initializing ML Model... (simulating 2s load time)")
            await asyncio.sleep(2)
            self._model_version = get_settings().MODEL_NAME
            self._is_loaded = True
            logger.info(f"Model {self._model_version} loaded successfully into memory.")

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    @property
    def version(self) -> str:
        return self._model_version

    def predict(self, text: str) -> dict:
        """
        Simulate text classification inference.
        Returns: { 'prediction': 'Positive'|'Negative'|'Neutral', 'confidence': float }
        """
        if not self._is_loaded:
            raise RuntimeError("Model is not loaded!")

        text_lower = text.lower()

        if any(word in text_lower for word in ["good", "great", "excellent", "love", "amazing", "happy"]):
            pred, conf = "Positive", round(random.uniform(0.75, 0.99), 4)
        elif any(word in text_lower for word in ["bad", "terrible", "awful", "hate", "worst", "sad"]):
            pred, conf = "Negative", round(random.uniform(0.75, 0.99), 4)
        else:
            pred, conf = "Neutral", round(random.uniform(0.40, 0.70), 4)

        return {"prediction": pred, "confidence": conf}


# Global singleton instance
ml_model = MLModelSingleton()


# ─── Service Functions ────────────────────────────────────────

class InferenceService:
    """Business logic layer for ML inference operations."""

    def __init__(self, db: AsyncSession):
        self.repo = InferenceRepository(db)

    async def run_inference(self, text: str) -> InferenceResult:
        """Run prediction and persist the result."""
        result = ml_model.predict(text)
        return await self.repo.create(
            text=text,
            prediction=result["prediction"],
            confidence=result["confidence"],
            model_version=ml_model.version,
        )

    async def get_inference_result(self, infer_id: int) -> InferenceResult | None:
        """Retrieve a past inference result by ID."""
        return await self.repo.get_by_id(infer_id)

    async def check_database_health(self) -> bool:
        """Delegate health check to the repository."""
        return await self.repo.check_health()
