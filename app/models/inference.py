# app/models/inference.py

from sqlalchemy import Column, DateTime, Float, Identity, Integer, String, Text
from sqlalchemy.sql import func

from app.db.base import Base


class InferenceResult(Base):
    """ORM model — stores MLOps text classification inference results."""

    __tablename__ = "mlops_inference_history"

    id = Column(Integer, Identity(start=1), primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    prediction = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    model_version = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<InferenceResult(id={self.id}, prediction='{self.prediction}', confidence={self.confidence})>"
