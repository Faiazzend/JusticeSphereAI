from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contract_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("contracts.id", ondelete="CASCADE"), nullable=True
    )
    agent_name: Mapped[str] = mapped_column(String(100))
    action: Mapped[str] = mapped_column(String(100))
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0)
    total_tokens: Mapped[int] = mapped_column(Integer, default=0)
    latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    model_name: Mapped[str] = mapped_column(String(100), default="fallback-simulator")
    estimated_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    contract: Mapped[Optional["Contract"]] = relationship(  # noqa: F821
        "Contract", back_populates="audit_logs"
    )
