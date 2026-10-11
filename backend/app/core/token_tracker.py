from typing import Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit import AuditLog


class TokenTracker:
    # Pricing per 1,000 tokens in USD: (prompt_rate, completion_rate)
    PRICING: Dict[str, tuple[float, float]] = {
        "gemini-3.5-flash-lite": (0.000075, 0.0003),
        "gemini": (0.000075, 0.0003),
        "gpt-4o": (0.005, 0.015),
        "openai": (0.005, 0.015),
        "claude-3-5-sonnet": (0.003, 0.015),
        "anthropic": (0.003, 0.015),
        "deepseek-r1": (0.00055, 0.00219),
        "ollama": (0.0, 0.0),
        "qwen3.5:4b": (0.0, 0.0),
        "default": (0.002, 0.008),
    }

    @staticmethod
    def estimate_tokens(text: str) -> int:
        if not text:
            return 0
        return max(1, len(text) // 4)

    @classmethod
    def calculate_cost(
        cls, prompt_tokens: int, completion_tokens: int, model_name: str
    ) -> float:
        model_key = model_name.lower()
        pricing_rate = None

        for k, v in cls.PRICING.items():
            if k in model_key:
                pricing_rate = v
                break

        if not pricing_rate:
            pricing_rate = cls.PRICING["default"]

        prompt_cost = (prompt_tokens / 1000.0) * pricing_rate[0]
        completion_cost = (completion_tokens / 1000.0) * pricing_rate[1]
        return round(prompt_cost + completion_cost, 6)

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
        model_name: str = "fallback-simulator",
        details: Optional[str] = None,
    ) -> AuditLog:
        prompt_tokens = cls.estimate_tokens(prompt_text)
        completion_tokens = cls.estimate_tokens(completion_text)
        total_tokens = prompt_tokens + completion_tokens
        cost_usd = cls.calculate_cost(prompt_tokens, completion_tokens, model_name)

        log_entry = AuditLog(
            contract_id=contract_id,
            agent_name=agent_name,
            action=action,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            latency_ms=round(latency_ms, 2),
            model_name=model_name,
            estimated_cost_usd=cost_usd,
            details=details,
        )

        db.add(log_entry)
        await db.commit()
        await db.refresh(log_entry)
        return log_entry


token_tracker = TokenTracker()
