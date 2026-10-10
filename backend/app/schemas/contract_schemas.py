from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class RedlineChange(BaseModel):
    id: str = Field(..., description="Unique ID for the redline change")
    section_number: str = Field(..., description="Section or clause identifier")
    original_text: str = Field(..., description="Original clause text from contract")
    suggested_text: str = Field(..., description="Redlined replacement text")
    diff_type: str = Field(..., description="INSERT, DELETE, or REPLACE")
    risk_severity: str = Field(default="MEDIUM", description="LOW, MEDIUM, HIGH, or CRITICAL")
    legal_rationale: str = Field(..., description="Legal rationale supporting this modification")
    accepted: Optional[bool] = Field(default=None, description="User decision: True, False, or None")


class DebateTurn(BaseModel):
    agent_name: str = Field(..., description="Auditor Agent, Opposing Counsel, or Redline Synthesizer")
    timestamp: str = Field(..., description="ISO timestamp")
    content: str = Field(..., description="Debate statement, objection, or compromise proposal")
    target_clause: Optional[str] = Field(default=None, description="Clause being debated")


class ContractUploadResponse(BaseModel):
    id: str
    title: str
    original_filename: str
    status: str
    message: str
    created_at: datetime


class ContractListItem(BaseModel):
    id: str
    title: str
    original_filename: str
    status: str
    playbook_name: str
    overall_risk_score: float
    created_at: datetime


class ContractDetailResponse(BaseModel):
    id: str
    title: str
    original_filename: str
    status: str
    error_message: Optional[str] = None
    playbook_name: str
    overall_risk_score: float
    risk_summary: Dict[str, Any]
    redlines: List[RedlineChange]
    obligations: List[Dict[str, Any]]
    debate_transcript: List[DebateTurn]
    created_at: datetime
    updated_at: datetime


class AnalysisTriggerRequest(BaseModel):
    playbook_name: Optional[str] = Field(default="Standard Corporate Playbook")
    use_local_llm: bool = Field(default=False)
    llm_provider: Optional[str] = Field(default=None, description="gemini, openai, anthropic, ollama, or auto")
    model_name: Optional[str] = Field(default=None, description="Specific model name override")
    api_key: Optional[str] = Field(default=None, description="Optional per-request API key override")
