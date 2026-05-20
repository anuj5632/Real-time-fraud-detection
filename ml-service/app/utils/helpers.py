from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def to_dict(obj: Any) -> Dict[str, Any]:
    if hasattr(obj, "dict"):
        return obj.dict(by_alias=True)
    if hasattr(obj, "model_dump"):
        return obj.model_dump(by_alias=True)
    raise TypeError("Unsupported object type")
