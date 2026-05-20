from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.config import settings
from app.model.train import train_model
from app.schemas.transaction_schema import TrainRequest, TrainResponse


@dataclass
class TrainingService:
    def train_model(self, request: TrainRequest) -> TrainResponse:
        data_path = Path(request.data_path) if request.data_path else settings.data_path
        metrics = train_model(data_path)
        return TrainResponse(model_version=settings.model_version, metrics=metrics)
