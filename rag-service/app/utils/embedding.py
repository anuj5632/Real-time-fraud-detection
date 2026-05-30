from __future__ import annotations

import hashlib
from typing import List

import numpy as np


def get_embedding(text: str, dim: int = 128) -> List[float]:
	"""Returns an embedding for text, using a lightweight hash-based fallback."""
	if not text:
		return [0.0] * dim

	try:
		from sentence_transformers import SentenceTransformer

		model = SentenceTransformer("all-MiniLM-L6-v2")
		vector = model.encode([text])[0]
		return vector.astype(float).tolist()
	except Exception:
		tokens = text.lower().split()
		vector = np.zeros(dim, dtype=float)
		for token in tokens:
			digest = hashlib.md5(token.encode("utf-8")).hexdigest()
			bucket = int(digest[:8], 16) % dim
			vector[bucket] += 1.0

		norm = float(np.linalg.norm(vector))
		if norm > 0.0:
			vector /= norm
		return vector.tolist()
