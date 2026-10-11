from typing import Optional
from pydantic import BaseModel, Field


class ObligationItem(BaseModel):
    id: str
    clause_reference: str
    obligor: str = Field(description="Responsible entity/party")
    recipient: str = Field(description="Beneficiary entity/party")
    obligation_type: str = Field(description="e.g. Notice, Escrow, Payment, SLA, Audit")
    description: str
    due_date_or_trigger: str
    recurrence: str = Field(description="One-time, Monthly, Quarterly, Annual, etc.")
    penalty_for_breach: str
    is_critical: bool = False
