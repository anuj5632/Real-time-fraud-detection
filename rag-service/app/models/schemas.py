from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TransactionInput(BaseModel):
	model_config = ConfigDict(populate_by_name=True)
	amount: float
	currency: str
	location: str
	device_id: str = Field(alias="deviceId")
	user_id: str = Field(alias="userId")
	status: Optional[str] = None
	created_at: Optional[datetime] = None


class ExplainRequest(BaseModel):
	transaction: TransactionInput
	fraud: bool
	probability: float


class ExplainResponse(BaseModel):
	explanation: str
