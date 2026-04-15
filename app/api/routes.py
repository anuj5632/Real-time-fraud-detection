from __future__ import annotations

from fastapi import APIRouter, Depends

from app.models.schemas import ExplainRequest, ExplainResponse
from app.services.generator import FraudExplanationGenerator
from app.services.rag_pipeline import RagPipeline
from app.services.retriever import Retriever

router = APIRouter()


def get_pipeline() -> RagPipeline:
	retriever = Retriever()
	generator = FraudExplanationGenerator()
	return RagPipeline(retriever=retriever, generator=generator)


@router.post("/explain", response_model=ExplainResponse)
def explain_transaction(request: ExplainRequest, pipeline: RagPipeline = Depends(get_pipeline)) -> ExplainResponse:
	explanation = pipeline.explain(request)
	return ExplainResponse(explanation=explanation)
