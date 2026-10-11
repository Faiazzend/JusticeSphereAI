import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String(255), default="Untitled Contract")
    original_filename: Mapped[str] = mapped_column(String(255), default="contract.pdf")
    file_path: Mapped[str] = mapped_column(String(512), default="")
    status: Mapped[str] = mapped_column(String(50), default="uploaded")
    overall_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    raw_text: Mapped[str] = mapped_column(Text, default="")
    playbook_name: Mapped[str] = mapped_column(
        String(100), default="Standard Corporate Playbook"
    )

    extracted_sections: Mapped[list] = mapped_column(JSON, default=list)
    identified_risks: Mapped[list] = mapped_column(JSON, default=list)
    debate_transcript: Mapped[list] = mapped_column(JSON, default=list)
    redlines: Mapped[list] = mapped_column(JSON, default=list)
    obligations: Mapped[list] = mapped_column(JSON, default=list)
    risk_summary: Mapped[dict] = mapped_column(
        JSON, default=lambda: {"critical": 0, "high": 0, "medium": 0, "low": 0}
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    audit_logs: Mapped[list["AuditLog"]] = relationship(  # noqa: F821
        "AuditLog", back_populates="contract", cascade="all, delete-orphan"
    )
