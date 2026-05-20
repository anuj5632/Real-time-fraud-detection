from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

import pandas as pd


@dataclass
class FeatureEngineer:
    user_stats: Dict[str, Dict[str, float]] = field(default_factory=dict)
    global_avg_amount: float = 0.0

    def fit(self, df: pd.DataFrame) -> "FeatureEngineer":
        if "user_id" not in df.columns or "amount" not in df.columns:
            self.user_stats = {}
            self.global_avg_amount = 0.0
            return self

        stats = df.groupby("user_id")["amount"].agg(["count", "mean"]).reset_index()
        self.user_stats = {
            row["user_id"]: {"count": float(row["count"]), "mean": float(row["mean"])}
            for _, row in stats.iterrows()
        }
        self.global_avg_amount = float(df["amount"].mean()) if not df.empty else 0.0
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        if "created_at" in df.columns:
            created = pd.to_datetime(df["created_at"], errors="coerce")
        else:
            created = pd.Series([pd.NaT] * len(df))
        df["transaction_hour"] = created.dt.hour.fillna(0).astype(int)

        def _count(uid: str) -> float:
            return self.user_stats.get(uid, {}).get("count", 1.0)

        def _mean(uid: str) -> float:
            return self.user_stats.get(uid, {}).get("mean", self.global_avg_amount)

        df["transaction_frequency"] = df["user_id"].map(_count).fillna(1.0)
        df["user_avg_amount"] = df["user_id"].map(_mean).fillna(self.global_avg_amount)
        return df
