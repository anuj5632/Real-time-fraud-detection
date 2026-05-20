from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


class Settings:
    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "fraud-ml-service")
        self.environment = os.getenv("ENV", "development")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

        self.data_dir = BASE_DIR / "data"
        self.data_path = Path(os.getenv("DATA_PATH", str(self.data_dir / "sample_transactions.csv")))

        self.model_dir = BASE_DIR / "models"
        self.model_path = Path(os.getenv("MODEL_PATH", str(self.model_dir / "xgboost_model.pkl")))
        self.model_version = os.getenv("MODEL_VERSION", "v1")
        self.feature_importance_path = Path(
            os.getenv("FEATURE_IMPORTANCE_PATH", str(self.model_dir / "feature_importance.json"))
        )

        self.mlflow_enabled = os.getenv("MLFLOW_ENABLED", "true").lower() == "true"
        self.mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
        self.mlflow_experiment = os.getenv("MLFLOW_EXPERIMENT", "fraud-detection")

        self.kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.kafka_consumer_group = os.getenv("KAFKA_CONSUMER_GROUP", "fraud-ml-service")
        self.kafka_input_topic = os.getenv("KAFKA_INPUT_TOPIC", "fraud-transactions")
        self.kafka_output_topic = os.getenv("KAFKA_OUTPUT_TOPIC", "fraud-results")


settings = Settings()
