from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.risk_schemas import RiskItem, RiskSummary, DebateTurn, RedlineItem
from app.schemas.obligation_schemas import ObligationItem


class ExtractedSection(BaseModel):
    section_number: str
    title: str
    content: str
    page_number: int = 1


class ContractBase(BaseModel):
    title: str
    playbook_name: str = "Standard Corporate Playbook"


class ContractCreate(ContractBase):
    original_filename: str
    file_path: str


class ContractSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    original_filename: str
    status: str
    overall_risk_score: float
    playbook_name: str
    risk_summary: RiskSummary
    created_at: datetime
    updated_at: datetime


class ContractDetailResponse(ContractSummaryResponse):
    model_config = ConfigDict(from_attributes=True)

    raw_text: str
    extracted_sections: List[Dict[str, Any]] = []
    identified_risks: List[Dict[str, Any]] = []
    debate_transcript: List[Dict[str, Any]] = []
    redlines: List[Dict[str, Any]] = []
    obligations: List[Dict[str, Any]] = []


class AnalysisTriggerRequest(BaseModel):
    playbook_name: Optional[str] = "Standard Corporate Playbook"
    use_local_llm: Optional[bool] = False
    llm_provider: Optional[str] = "gemini"
    model_name: Optional[str] = "gemini-2.0-flash"
    api_key_override: Optional[str] = None


class AuditSummaryResponse(BaseModel):
    total_tokens: int
    total_cost_usd: float
    avg_latency_ms: float
    total_runs: int
    by_agent: Dict[str, Dict[str, Any]]


class LLMConfigResponse(BaseModel):
    gemini_configured: bool
    openai_configured: bool
    anthropic_configured: bool
    ollama_endpoint: str
    active_provider: str
    active_model: str


class LLMConfigUpdateRequest(BaseModel):
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    ollama_base_url: Optional[str] = None
    active_provider: Optional[str] = None
    active_model: Optional[str] = None


class ProviderHealth(BaseModel):
    available: bool
    latency_ms: float
    message: str


class LLMHealthResponse(BaseModel):
    status: str
    active_provider: str
    providers: Dict[str, ProviderHealth]


from pydantic import BaseModel, Field, ConfigDict, model_validator


class ContractCompareRequest(BaseModel):
    base_contract_id: Optional[str] = None
    source_contract_id: Optional[str] = None
    target_contract_id: str

    @model_validator(mode="after")
    def resolve_base_id(self):
        if not self.base_contract_id and not self.source_contract_id:
            raise ValueError("Either base_contract_id or source_contract_id must be provided")
        if not self.base_contract_id:
            self.base_contract_id = self.source_contract_id
        return self


class SectionDiffItem(BaseModel):
    section_title: str
    status: str
    diff_tokens: List[Dict[str, str]]


class ContractCompareResponse(BaseModel):
    base_id: str
    base_title: str
    target_id: str
    target_title: str
    base_risk_score: float
    target_risk_score: float
    risk_score_delta: float
    sections: List[SectionDiffItem]
    source_id: Optional[str] = None
    source_title: Optional[str] = None
    source_risk_score: Optional[float] = None
    risk_delta: Optional[float] = None
