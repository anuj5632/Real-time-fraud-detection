from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd

from app.model.model_loader import load_bundle
from app.model.predict import predict_proba
from app.schemas.transaction_schema import (
    BatchPredictionRequest,
    BatchPredictionResponse,
    PredictionResponse,
    TransactionRequest,
)
from app.utils.helpers import to_dict


@dataclass
class InferenceService:
    fraud_threshold: float = 0.8
    review_threshold: float = 0.5

    def _decision(self, probability: float) -> str:
        if probability >= self.fraud_threshold:
            return "FRAUD"
        if probability >= self.review_threshold:
            return "REVIEW"
        return "SUCCESS"

    def predict_single(self, request: TransactionRequest) -> PredictionResponse:
        df = pd.DataFrame([request.model_dump(by_alias=False)])
        probability = float(predict_proba(df).iloc[0])
        decision = self._decision(probability)

        bundle = load_bundle()
        return PredictionResponse(
            fraud=probability >= self.fraud_threshold,
            probability=probability,
            decision=decision,
            model_version=bundle.model_version,
        )

    def predict_batch(self, request: BatchPredictionRequest) -> BatchPredictionResponse:
        records = [tx.model_dump(by_alias=False) for tx in request.transactions]
        df = pd.DataFrame(records)
        probabilities = predict_proba(df)

        bundle = load_bundle()
        results: List[PredictionResponse] = []
        for prob in probabilities:
            decision = self._decision(float(prob))
            results.append(
                PredictionResponse(
                    fraud=float(prob) >= self.fraud_threshold,
                    probability=float(prob),
                    decision=decision,
                    model_version=bundle.model_version,
                )
            )
        return BatchPredictionResponse(results=results)
