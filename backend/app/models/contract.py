import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, Text, JSON, Boolean
from app.database import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    status = Column(String(50), default="uploaded", nullable=False)  # uploaded, processing, analyzed, error
    error_message = Column(Text, nullable=True)
    raw_text = Column(Text, nullable=True)
    playbook_name = Column(String(100), default="Standard Corporate Playbook", nullable=False)
    overall_risk_score = Column(Float, default=0.0, nullable=False)
    
    # Structured extractions & results stored as JSON
    extracted_sections = Column(JSON, default=list, nullable=False)
    identified_risks = Column(JSON, default=list, nullable=False)
    debate_transcript = Column(JSON, default=list, nullable=False)
    redlines = Column(JSON, default=list, nullable=False)
    obligations = Column(JSON, default=list, nullable=False)
    risk_summary = Column(JSON, default=dict, nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class Playbook(Base):
    __tablename__ = "playbooks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    rules = Column(JSON, default=list, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
