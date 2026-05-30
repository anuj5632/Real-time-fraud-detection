from __future__ import annotations

from dataclasses import dataclass

from app.models.schemas import ExplainRequest
from app.services.generator import ExplanationInput, FraudExplanationGenerator
from app.services.retriever import Retriever


@dataclass
class RagPipeline:
	retriever: Retriever
	generator: FraudExplanationGenerator

	def explain(self, request: ExplainRequest) -> str:
		query = self._transaction_to_query(request)
		retrieved = self.retriever.retrieve(query)
		payload = ExplanationInput(
			amount=request.transaction.amount,
			currency=request.transaction.currency,
			location=request.transaction.location,
			device_id=request.transaction.device_id,
			user_id=request.transaction.user_id,
			status=request.transaction.status,
			fraud=request.fraud,
			probability=request.probability,
			retrieved_context=retrieved,
		)
		return self.generator.generate_explanation(payload)

	@staticmethod
	def _transaction_to_query(request: ExplainRequest) -> str:
		transaction = request.transaction
		return (
			f"amount={transaction.amount} currency={transaction.currency} "
			f"location={transaction.location} device_id={transaction.device_id} "
			f"user_id={transaction.user_id} fraud={request.fraud} "
			f"probability={request.probability}"
		)
