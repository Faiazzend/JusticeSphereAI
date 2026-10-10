import time
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit import AuditLog


class TokenTracker:
    """Tracks token consumption, latency, and estimated cloud costs."""

    # Cost per 1k tokens in USD (rates as of 2026/standard)
    PRICING_PER_1K = {
        "gpt-4o": {"prompt": 0.005, "completion": 0.015},
        "claude-3-5-sonnet": {"prompt": 0.003, "completion": 0.015},
        "deepseek-r1": {"prompt": 0.00055, "completion": 0.00219},
        "gemini-3.5-flash-lite": {"prompt": 0.000075, "completion": 0.0003},
        "gemini-flash": {"prompt": 0.000075, "completion": 0.0003},
        "gemini-pro": {"prompt": 0.00125, "completion": 0.005},
        "gemini": {"prompt": 0.000075, "completion": 0.0003},
        "google": {"prompt": 0.000075, "completion": 0.0003},
        "ollama": {"prompt": 0.0, "completion": 0.0},
        "default": {"prompt": 0.002, "completion": 0.008}
    }

    @classmethod
    def estimate_tokens(cls, text: str) -> int:
        """Heuristic token count based on standard ~4 characters per token."""
        if not text:
            return 0
        return max(1, len(text) // 4)

    @classmethod
    def calculate_cost(cls, model_name: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate USD expenditure based on model and token counts."""
        model_lower = model_name.lower()
        key = "default"
        for candidate in cls.PRICING_PER_1K:
            if candidate in model_lower:
                key = candidate
                break

        rates = cls.PRICING_PER_1K[key]
        cost = (prompt_tokens / 1000.0 * rates["prompt"]) + (completion_tokens / 1000.0 * rates["completion"])
        return round(cost, 6)

    @classmethod
    async def log_execution(
        cls,
        db: AsyncSession,
        contract_id: Optional[str],
        agent_name: str,
        action: str,
        prompt_text: str,
        completion_text: str,
        latency_ms: float,
        model_name: str,
        details: Optional[str] = None
    ) -> AuditLog:
        """Create and commit an audit log entry."""
        prompt_tokens = cls.estimate_tokens(prompt_text)
        completion_tokens = cls.estimate_tokens(completion_text)
        total_tokens = prompt_tokens + completion_tokens
        cost = cls.calculate_cost(model_name, prompt_tokens, completion_tokens)

        audit_entry = AuditLog(
            contract_id=contract_id,
            agent_name=agent_name,
            action=action,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            latency_ms=round(latency_ms, 2),
            model_name=model_name,
            estimated_cost_usd=cost,
            details=details
        )
        db.add(audit_entry)
        await db.commit()
        await db.refresh(audit_entry)
        return audit_entry


token_tracker = TokenTracker()
