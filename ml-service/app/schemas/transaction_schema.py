from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    id: Optional[str] = None
    amount: float
    currency: str
    location: str
    device_id: str = Field(alias="deviceId")
    user_id: str = Field(alias="userId")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    status: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class PredictionResponse(BaseModel):
    fraud: bool
    probability: float
    decision: str
    model_version: str = Field(alias="modelVersion")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class BatchPredictionRequest(BaseModel):
    transactions: List[TransactionRequest]


class BatchPredictionResponse(BaseModel):
    results: List[PredictionResponse]


class TrainRequest(BaseModel):
    data_path: Optional[str] = None


class TrainResponse(BaseModel):
    model_version: str = Field(alias="modelVersion")
    metrics: dict

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
