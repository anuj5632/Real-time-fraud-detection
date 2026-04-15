from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple

import numpy as np


@dataclass
class VectorRecord:
	text: str
	embedding: List[float]


class InMemoryVectorStore:
	"""Simple in-memory vector store for lightweight similarity search."""

	def __init__(self) -> None:
		self._records: list[VectorRecord] = []

	def add(self, text: str, embedding: List[float]) -> None:
		self._records.append(VectorRecord(text=text, embedding=embedding))

	def bulk_add(self, records: Iterable[Tuple[str, List[float]]]) -> None:
		for text, embedding in records:
			self.add(text, embedding)

	def search(self, query_embedding: List[float], top_k: int = 5) -> list[str]:
		if not self._records:
			return []

		query = np.array(query_embedding, dtype=float)
		query_norm = float(np.linalg.norm(query))
		if query_norm == 0.0:
			return [record.text for record in self._records[:top_k]]

		scored = []
		for record in self._records:
			vector = np.array(record.embedding, dtype=float)
			denom = float(np.linalg.norm(vector) * query_norm)
			score = float(vector.dot(query) / denom) if denom > 0.0 else 0.0
			scored.append((score, record.text))

		scored.sort(key=lambda item: item[0], reverse=True)
		return [text for _, text in scored[:top_k]]
