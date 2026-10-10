from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class PlaybookRule(BaseModel):
    category: str = Field(..., description="e.g. Indemnification, Limitation of Liability, IP, Governing Law")
    standard_requirement: str = Field(..., description="The Gold Standard expected policy")
    unacceptable_terms: List[str] = Field(default_factory=list, description="Terms that trigger high/critical risk")
    preferred_fallback: str = Field(..., description="Approved compromise fallback clause")
    severity_if_missing: str = Field(default="HIGH", description="LOW, MEDIUM, HIGH, CRITICAL")


class PlaybookCreate(BaseModel):
    name: str
    description: Optional[str] = None
    rules: List[PlaybookRule]
    is_default: bool = False


class PlaybookResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    rules: List[PlaybookRule]
    is_default: bool
    created_at: datetime
