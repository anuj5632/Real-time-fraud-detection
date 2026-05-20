from __future__ import annotations

from contextlib import contextmanager
from typing import Dict, Optional

import mlflow

from app.utils.logger import get_logger

logger = get_logger(__name__)


class MLflowRun:
    def __init__(self, run) -> None:
        self.run = run

    def log_params(self, params: Dict[str, float]) -> None:
        mlflow.log_params(params)

    def log_metrics(self, metrics: Dict[str, float]) -> None:
        mlflow.log_metrics(metrics)

    def log_model(self, model, artifact_path: str) -> None:
        mlflow.xgboost.log_model(model, artifact_path)

    def log_dict(self, payload: Dict, artifact_file: str) -> None:
        mlflow.log_dict(payload, artifact_file)


@contextmanager
def mlflow_run(enabled: bool, experiment: str, tracking_uri: str):
    if not enabled:
        yield None
        return

    try:
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment)
        run = mlflow.start_run()
        yield MLflowRun(run)
    except Exception:
        logger.exception("MLflow tracking failed")
        yield None
    finally:
        try:
            mlflow.end_run()
        except Exception:
            pass
