from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, model_validator


class PlaybookRule(BaseModel):
    category: str
    severity: Optional[str] = "HIGH"
    preferred_position: Optional[str] = ""
    fallback_position: Optional[str] = ""
    hard_stop: Optional[str] = ""
    rule_id: Optional[str] = None
    standard_position: Optional[str] = None


class Playbook(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    rules: List[PlaybookRule] = Field(default_factory=list)
    risk_tolerance: Optional[float] = None

    @model_validator(mode="after")
    def ensure_id(self):
        if not self.id:
            self.id = self.name.lower().replace(" ", "_").replace("-", "_")
        return self
