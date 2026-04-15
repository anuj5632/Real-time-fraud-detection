from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import Any, Iterable, List


@dataclass
class ExplanationInput:
	amount: float
	currency: str
	location: str
	device_id: str
	user_id: str
	status: str | None
	fraud: bool
	probability: float
	retrieved_context: str | Iterable[str]


class FraudExplanationGenerator:
	"""Builds prompts and generates simple explanations for fraud decisions."""

	_PROMPT_TEMPLATE = """You are an AI fraud detection assistant integrated into a real-time fintech system.

Your task is to generate a clear, concise, and human-readable explanation for why a transaction was flagged as fraudulent or legitimate.

---

## Transaction Details:

* Amount: {amount}
* Currency: {currency}
* Location: {location}
* Device ID: {device_id}
* User ID: {user_id}
* Transaction Status: {status}

---

## ML Prediction:

* Fraud: {fraud}
* Probability: {probability}

---

## Retrieved Context (from similar fraud cases and rules):

{retrieved_context}

---

## Instructions:

1. Analyze the transaction details along with the ML prediction.
2. Use the retrieved context (past fraud cases, rules, or patterns) to support reasoning.
3. Focus on behavioral anomalies such as:
   * Unusual transaction amount
   * Suspicious location
   * Unknown or untrusted device
   * Deviation from normal user behavior
4. If fraud is TRUE:
   * Clearly explain why the transaction is suspicious
5. If fraud is FALSE:
   * Explain why the transaction appears normal
6. Keep explanation:
   * Simple (non-technical)
   * 2-3 lines maximum
   * Suitable for end-users or analysts

---

## Output Format:

Return ONLY a JSON response:

{{
"explanation": "Your explanation here"
}}

Do NOT include any extra text outside JSON.
"""

	def build_prompt(self, payload: ExplanationInput) -> str:
		return self._PROMPT_TEMPLATE.format(
			amount=payload.amount,
			currency=payload.currency,
			location=payload.location,
			device_id=payload.device_id,
			user_id=payload.user_id,
			status=payload.status or "UNKNOWN",
			fraud=str(payload.fraud).lower(),
			probability=payload.probability,
			retrieved_context=self._normalize_context(payload.retrieved_context),
		)

	def generate_explanation(self, payload: ExplanationInput) -> str:
		"""Generates a concise explanation without calling an external LLM."""
		reasons = self._build_reasons(payload)
		base = (
			"This transaction looks suspicious" if payload.fraud else "This transaction appears normal"
		)
		if reasons:
			summary = f"{base} because {', '.join(reasons)}."
		else:
			summary = f"{base} based on the details and retrieved context."

		context_hint = self._context_hint(payload.retrieved_context)
		explanation = f"{summary}\n{context_hint}" if context_hint else summary
		return self._clamp_lines(explanation, max_lines=3)

	def normalize_model_response(self, raw_response: str, fraud: bool) -> dict[str, str]:
		parsed = self._extract_json(raw_response)
		explanation = ""
		if isinstance(parsed, dict):
			value = parsed.get("explanation")
			if isinstance(value, str):
				explanation = value.strip()

		if not explanation:
			explanation = self._fallback_explanation(fraud)

		explanation = self._clamp_lines(explanation, max_lines=3)
		return {"explanation": explanation}

	def response_to_json(self, explanation: str) -> str:
		safe_explanation = self._clamp_lines((explanation or "").strip(), max_lines=3)
		if not safe_explanation:
			safe_explanation = "This transaction appears normal based on available details and context."
		return json.dumps({"explanation": safe_explanation}, ensure_ascii=True)

	@staticmethod
	def _build_reasons(payload: ExplanationInput) -> list[str]:
		reasons: list[str] = []
		if payload.amount >= 10000:
			reasons.append("the amount is unusually high")
		if payload.probability >= 0.85:
			reasons.append("the risk score is high")

		context = " ".join(FraudExplanationGenerator._context_items(payload.retrieved_context)).lower()
		if "untrusted" in context or "unknown device" in context:
			reasons.append("the device appears untrusted")
		if "unusual location" in context or "location mismatch" in context:
			reasons.append("the location differs from typical activity")

		return reasons

	@staticmethod
	def _context_hint(retrieved_context: str | Iterable[str]) -> str:
		items = FraudExplanationGenerator._context_items(retrieved_context)
		if not items:
			return ""

		top = items[0]
		return f"Context: {top}"

	@staticmethod
	def _context_items(retrieved_context: str | Iterable[str]) -> list[str]:
		if isinstance(retrieved_context, str):
			return [line.strip() for line in retrieved_context.splitlines() if line.strip()]

		return [str(item).strip() for item in retrieved_context if str(item).strip()]

	@staticmethod
	def _normalize_context(retrieved_context: str | Iterable[str]) -> str:
		if isinstance(retrieved_context, str):
			context = retrieved_context.strip()
			return context if context else "No related cases or rules were retrieved."

		items = [str(item).strip() for item in retrieved_context if str(item).strip()]
		if not items:
			return "No related cases or rules were retrieved."
		return "\n".join(f"- {item}" for item in items)

	@staticmethod
	def _extract_json(raw_response: str) -> dict[str, Any] | None:
		if not raw_response:
			return None

		candidate = raw_response.strip()
		try:
			parsed = json.loads(candidate)
			return parsed if isinstance(parsed, dict) else None
		except json.JSONDecodeError:
			pass

		match = re.search(r"\{[\s\S]*\}", candidate)
		if not match:
			return None

		try:
			parsed = json.loads(match.group(0))
			return parsed if isinstance(parsed, dict) else None
		except json.JSONDecodeError:
			logging.warning("Failed to parse model JSON response.")
			return None

	@staticmethod
	def _fallback_explanation(fraud: bool) -> str:
		if fraud:
			return (
				"This transaction looks suspicious due to unusual behavior compared with normal activity "
				"and similar fraud cases."
			)
		return (
			"This transaction appears legitimate because its behavior matches expected user patterns "
			"and known safe activity."
		)

	@staticmethod
	def _clamp_lines(text: str, max_lines: int) -> str:
		lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
		if not lines:
			return ""
		return "\n".join(lines[:max_lines])
