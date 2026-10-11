from typing import List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict


class DiffToken(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: str = Field(description="'equal', 'insert', or 'delete'")
    text: str


class RiskItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    category: str
    severity: str = Field(description="CRITICAL, HIGH, MEDIUM, or LOW")
    score: float = Field(default=0.0, ge=0.0, le=100.0)
    clause_reference: str
    original_text: str
    legal_rationale: str
    mitigation_strategy: str


class RiskSummary(BaseModel):
    model_config = ConfigDict(extra="allow")
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0


class DebateTurn(BaseModel):
    model_config = ConfigDict(extra="allow")
    agent_name: str
    timestamp: str
    content: str
    target_clause: Optional[str] = None


class RedlineItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    section_number: str
    original_text: str
    suggested_text: str
    diff_type: str = "Modification"
    risk_severity: str = "HIGH"
    legal_rationale: str
    diff_tokens: List[DiffToken] = []
    accepted: Optional[bool] = None  # None: Pending, True: Accepted, False: Rejected
    custom_prompt: Optional[str] = None

    # Backward compatibility properties if accessed
    clause_id: Optional[str] = None
    category: Optional[str] = None
    revised_text: Optional[str] = None
    consensus_score: Optional[float] = None


class RedlineDecisionUpdateRequest(BaseModel):
    accepted: Optional[bool] = None


class RedlineRegenerateRequest(BaseModel):
    custom_prompt: str
    provider: Optional[str] = None
    model_name: Optional[str] = None
