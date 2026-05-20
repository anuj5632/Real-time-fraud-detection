from fastapi import APIRouter, HTTPException

from app.schemas.transaction_schema import (
    BatchPredictionRequest,
    BatchPredictionResponse,
    PredictionResponse,
    TrainRequest,
    TrainResponse,
    TransactionRequest,
)
from app.services.inference_service import InferenceService
from app.services.training_service import TrainingService
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

inference_service = InferenceService()
training_service = TrainingService()


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@router.post("/predict", response_model=PredictionResponse, response_model_by_alias=True)
def predict(request: TransactionRequest) -> PredictionResponse:
    try:
        return inference_service.predict_single(request)
    except Exception as exc:  # pragma: no cover - generic safety net
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/predict/batch", response_model=BatchPredictionResponse, response_model_by_alias=True)
def predict_batch(request: BatchPredictionRequest) -> BatchPredictionResponse:
    try:
        return inference_service.predict_batch(request)
    except Exception as exc:  # pragma: no cover - generic safety net
        logger.exception("Batch prediction failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/train", response_model=TrainResponse, response_model_by_alias=True)
def train(request: TrainRequest) -> TrainResponse:
    try:
        return training_service.train_model(request)
    except Exception as exc:  # pragma: no cover - generic safety net
        logger.exception("Training failed")
        raise HTTPException(status_code=500, detail=str(exc))
