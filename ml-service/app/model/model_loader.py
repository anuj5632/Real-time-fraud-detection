from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import joblib

from app.config import settings
from app.utils.helpers import ensure_dir


@dataclass
class ModelBundle:
    model: Any
    preprocessor: Any
    feature_engineer: Any
    feature_columns: list
    model_version: str
    feature_names: list | None = None


def save_bundle(bundle: ModelBundle, model_path: Path | None = None) -> Path:
    path = model_path or settings.model_path
    ensure_dir(path.parent)
    joblib.dump(bundle, path)
    return path


def load_bundle(model_path: Path | None = None) -> ModelBundle:
    path = model_path or settings.model_path
    if not path.exists():
        raise FileNotFoundError(f"Model not found at {path}")
    try:
        return joblib.load(path)
    except Exception as exc:  # pragma: no cover - safety net
        raise RuntimeError("Failed to load model bundle. Train the model first.") from exc
