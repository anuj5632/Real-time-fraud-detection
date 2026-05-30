from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	app_name: str = "rag-service"
	api_prefix: str = ""
	data_dir: Path = Path(__file__).resolve().parent.parent / "data"
	fraud_rules_path: Path = data_dir / "fraud_rules.txt"
	sample_cases_path: Path = data_dir / "sample_cases.json"
	embedding_dim: int = 128
	retriever_top_k: int = 5


@lru_cache
def get_settings() -> Settings:
	return Settings()
