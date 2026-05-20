from __future__ import annotations

from pathlib import Path
import json
from typing import Dict, List

import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from app.config import settings
from app.mlflow.tracking import mlflow_run
from app.model.evaluate import evaluate_predictions
from app.model.model_loader import ModelBundle, save_bundle
from app.model.preprocess import build_preprocessor, clean_missing, split_features_target
from app.utils.feature_engineering import FeatureEngineer
from app.utils.logger import get_logger

logger = get_logger(__name__)

TARGET_COLUMN = "is_fraud"
CATEGORICAL_FEATURES = ["currency", "location", "device_id"]
NUMERIC_FEATURES = [
    "amount",
    "transaction_hour",
    "transaction_frequency",
    "user_avg_amount",
]
FEATURE_COLUMNS = CATEGORICAL_FEATURES + NUMERIC_FEATURES


def load_dataset(data_path: Path) -> pd.DataFrame:
    return pd.read_csv(data_path)


def train_model(data_path: Path | None = None) -> Dict[str, float]:
    data_path = data_path or settings.data_path
    logger.info("Loading dataset from %s", data_path)
    df = load_dataset(data_path)

    df = clean_missing(df)

    feature_engineer = FeatureEngineer().fit(df)
    df = feature_engineer.transform(df)

    x, y = split_features_target(df, TARGET_COLUMN, FEATURE_COLUMNS)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    preprocessor = build_preprocessor(NUMERIC_FEATURES, CATEGORICAL_FEATURES)
    x_train_processed = preprocessor.fit_transform(x_train)
    x_test_processed = preprocessor.transform(x_test)

    positives = max(float((y_train == 1).sum()), 1.0)
    negatives = max(float((y_train == 0).sum()), 1.0)
    scale_pos_weight = negatives / positives

    model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        objective="binary:logistic",
        eval_metric="logloss",
        scale_pos_weight=scale_pos_weight,
        random_state=42,
    )

    model.fit(x_train_processed, y_train)

    y_prob = model.predict_proba(x_test_processed)[:, 1]
    metrics = evaluate_predictions(y_test, y_prob)

    feature_names: List[str] = list(preprocessor.get_feature_names_out())
    importance_scores = model.feature_importances_.tolist()
    importance = sorted(
        zip(feature_names, importance_scores),
        key=lambda item: item[1],
        reverse=True,
    )
    top_features = [{"feature": name, "importance": float(score)} for name, score in importance[:25]]
    settings.feature_importance_path.parent.mkdir(parents=True, exist_ok=True)
    settings.feature_importance_path.write_text(json.dumps(top_features, indent=2))

    model_bundle = ModelBundle(
        model=model,
        preprocessor=preprocessor,
        feature_engineer=feature_engineer,
        feature_columns=FEATURE_COLUMNS,
        model_version=settings.model_version,
        feature_names=feature_names,
    )
    save_bundle(model_bundle)

    with mlflow_run(
        enabled=settings.mlflow_enabled,
        experiment=settings.mlflow_experiment,
        tracking_uri=settings.mlflow_tracking_uri,
    ) as run:
        if run:
            run.log_params(
                {
                    "n_estimators": 300,
                    "max_depth": 6,
                    "learning_rate": 0.05,
                    "subsample": 0.9,
                    "colsample_bytree": 0.9,
                    "scale_pos_weight": scale_pos_weight,
                }
            )
            numeric_metrics = {k: v for k, v in metrics.items() if isinstance(v, (int, float))}
            run.log_metrics(numeric_metrics)
            run.log_dict({"confusion_matrix": metrics.get("confusion_matrix", [])}, "confusion_matrix.json")
            run.log_dict({"feature_importance": top_features}, "feature_importance.json")
            run.log_model(model, "xgboost-model")

    logger.info("Training complete with metrics: %s", metrics)
    return metrics
