from typing import List, Optional
from pydantic import BaseModel, Field


class PlaybookRule(BaseModel):
    category: str
    severity: str
    preferred_position: str
    fallback_position: str
    hard_stop: str


class Playbook(BaseModel):
    id: str
    name: str
    description: str
    rules: List[PlaybookRule]
