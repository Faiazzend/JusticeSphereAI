from typing import TypedDict, List, Dict, Any, Optional


class ContractReviewState(TypedDict):
    contract_id: str
    contract_title: str
    raw_text: str
    sections: List[Dict[str, Any]]
    playbook_rules: List[Dict[str, Any]]
    debate_cycle: int
    max_debate_cycles: int
    use_local_llm: bool
    llm_provider: Optional[str]
    model_name: Optional[str]
    api_key_override: Optional[str]
    
    # Evolving agent data
    identified_risks: List[Dict[str, Any]]
    debate_transcript: List[Dict[str, Any]]
    redlines: List[Dict[str, Any]]
    obligations: List[Dict[str, Any]]
    risk_summary: Dict[str, Any]
    overall_score: float
    current_status: str
    error: Optional[str]
