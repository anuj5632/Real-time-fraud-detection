from __future__ import annotations

import pandas as pd

from app.model.model_loader import load_bundle
from app.model.preprocess import clean_missing
from app.utils.logger import get_logger

logger = get_logger(__name__)


def predict_proba(df: pd.DataFrame) -> pd.Series:
    bundle = load_bundle()

    df = clean_missing(df)
    df = bundle.feature_engineer.transform(df)
    x = df[bundle.feature_columns]
    x_processed = bundle.preprocessor.transform(x)

    probabilities = bundle.model.predict_proba(x_processed)[:, 1]
    return pd.Series(probabilities)
