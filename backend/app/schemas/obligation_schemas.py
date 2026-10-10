from typing import List
from pydantic import BaseModel, Field


class ObligationItem(BaseModel):
    id: str = Field(..., description="Unique obligation ID (e.g., obl_001)")
    clause_reference: str = Field(..., description="Section or clause citation in the contract")
    obligor: str = Field(..., description="The party responsible for performing the duty")
    recipient: str = Field(..., description="The beneficiary party of the obligation")
    obligation_type: str = Field(..., description="Payment | Insurance | Delivery | Audit | Termination | Confidentiality")
    description: str = Field(..., description="Clear explanation of the required performance")
    due_date_or_trigger: str = Field(..., description="Specific date or condition trigger")
    recurrence: str = Field(default="One-time", description="One-time, Monthly, Quarterly, Annual, or Upon Trigger")
    penalty_for_breach: str = Field(..., description="Remedies, penalties, or consequences of failure")
    is_critical: bool = Field(default=False, description="Flag indicating if breach causes material failure or termination")


class ObligationsResponse(BaseModel):
    contract_id: str
    summary: str
    overall_risk_score: float
    obligations: List[ObligationItem]
