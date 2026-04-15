from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Iterable, List

from app.config import get_settings
from app.db.chroma_client import InMemoryVectorStore
from app.utils.embedding import get_embedding


class Retriever:
	"""Loads fraud rules and sample cases to retrieve relevant context."""

	def __init__(self, rules_path: Path | None = None, cases_path: Path | None = None) -> None:
		settings = get_settings()
		self._rules_path = rules_path or settings.fraud_rules_path
		self._cases_path = cases_path or settings.sample_cases_path
		self._store = InMemoryVectorStore()
		self._loaded = False

	def load(self) -> None:
		if self._loaded:
			return

		for text in self._load_rules():
			self._store.add(text, get_embedding(text))

		for text in self._load_cases():
			self._store.add(text, get_embedding(text))

		self._loaded = True

	def retrieve(self, query: str, top_k: int | None = None) -> list[str]:
		self.load()
		settings = get_settings()
		count = top_k or settings.retriever_top_k

		if not query:
			return self._fallback_context()

		results = self._store.search(get_embedding(query), top_k=count)
		if results:
			return results
		return self._fallback_context()

	def _load_rules(self) -> Iterable[str]:
		if not self._rules_path.exists():
			logging.warning("Fraud rules file not found: %s", self._rules_path)
			return []

		lines = [line.strip() for line in self._rules_path.read_text(encoding="utf-8").splitlines()]
		return [line for line in lines if line]

	def _load_cases(self) -> Iterable[str]:
		if not self._cases_path.exists():
			logging.warning("Sample cases file not found: %s", self._cases_path)
			return []

		raw = self._cases_path.read_text(encoding="utf-8").strip()
		if not raw:
			return []

		try:
			data = json.loads(raw)
		except json.JSONDecodeError:
			logging.warning("Sample cases JSON is invalid.")
			return []

		if isinstance(data, list):
			return [self._case_to_text(item) for item in data]

		return [self._case_to_text(data)]

	def _case_to_text(self, item: object) -> str:
		if isinstance(item, str):
			return item
		if isinstance(item, dict):
			details = ", ".join(f"{key}={value}" for key, value in item.items())
			return f"Case: {details}"
		return str(item)

	def _fallback_context(self) -> list[str]:
		return [
			"No close matches were found in stored fraud rules or cases.",
			"Use transaction details and model score to explain the decision.",
		]
