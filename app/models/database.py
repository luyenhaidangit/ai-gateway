from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from app.database import Base


class InferenceResult(Base):
    """ORM model — stores MLOps text classification inference results."""

    __tablename__ = "inference_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    prediction = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    model_version = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<InferenceResult(id={self.id}, prediction='{self.prediction}', confidence={self.confidence})>"
