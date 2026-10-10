from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class RiskItem(BaseModel):
    id: str = Field(..., description="Unique risk identifier")
    clause_reference: str = Field(..., description="Section citation")
    category: str = Field(..., description="e.g. Indemnification, Limitation of Liability, IP, Termination")
    severity: str = Field(..., description="LOW, MEDIUM, HIGH, CRITICAL")
    score: float = Field(..., ge=0.0, le=100.0, description="Risk score contribution")
    rationale: str = Field(..., description="Why this clause presents legal/operational risk")
    suggested_mitigation: str = Field(..., description="Contractual counter-clause or playbook resolution")


class RiskSummary(BaseModel):
    overall_score: float = Field(..., ge=0.0, le=100.0)
    critical_count: int = Field(default=0)
    high_count: int = Field(default=0)
    medium_count: int = Field(default=0)
    low_count: int = Field(default=0)
    category_scores: Dict[str, float] = Field(default_factory=dict)
