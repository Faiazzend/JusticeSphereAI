import time
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config import settings
from app.models.contract import Contract
from app.agents.state import ContractReviewState
from app.agents.nodes.auditor_agent import auditor_node
from app.agents.nodes.opposing_agent import opposing_node
from app.agents.nodes.redline_agent import redline_node
from app.agents.nodes.obligation_agent import obligation_node
from app.core.token_tracker import token_tracker


class ContractReviewOrchestrator:
    """
    Executes the multi-agent legal debate and review pipeline.
    Connects: Auditor -> Opposing Counsel -> Redline Synthesizer -> Obligation Extractor.
    """

    @classmethod
    async def run(
        cls,
        contract_id: str,
        contract_title: str,
        raw_text: str,
        sections: List[Dict[str, Any]],
        playbook_rules: List[Dict[str, Any]],
        use_local_llm: bool,
        db: AsyncSession,
        llm_provider: Optional[str] = None,
        model_name: Optional[str] = None,
        api_key_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end multi-agent review and persists results to the database.
        """
        start_time = time.time()
        
        # Initial State
        state: ContractReviewState = {
            "contract_id": contract_id,
            "contract_title": contract_title,
            "raw_text": raw_text,
            "sections": sections,
            "playbook_rules": playbook_rules,
            "debate_cycle": 1,
            "max_debate_cycles": 2,
            "use_local_llm": use_local_llm,
            "llm_provider": llm_provider,
            "model_name": model_name,
            "api_key_override": api_key_override,
            "identified_risks": [],
            "debate_transcript": [],
            "redlines": [],
            "obligations": [],
            "risk_summary": {},
            "overall_score": 0.0,
            "current_status": "Starting review",
            "error": None
        }

        # Determine active model name for token logging
        if use_local_llm or llm_provider == "ollama":
            active_model = f"ollama/{model_name or settings.FALLBACK_MODEL}"
        elif llm_provider == "gemini" or (settings.GEMINI_API_KEY and not settings.OPENAI_API_KEY):
            active_model = f"google/{model_name or 'gemini-3.5-flash-lite'}"
        elif llm_provider in ("openai", "codex") or settings.OPENAI_API_KEY:
            active_model = f"openai/{model_name or settings.DEFAULT_MODEL}"
        elif llm_provider == "anthropic" or settings.ANTHROPIC_API_KEY:
            active_model = f"anthropic/{model_name or 'claude-3-5-sonnet'}"
        else:
            active_model = "heuristic-legal-engine"

        # 1. Auditor Node
        t0 = time.time()
        auditor_res = await auditor_node(state)
        t1 = time.time()
        state.update(auditor_res)
        await token_tracker.log_execution(
            db=db,
            contract_id=contract_id,
            agent_name="Auditor Agent",
            action="audit_risks",
            prompt_text=f"Review sections for {contract_title}",
            completion_text=str(state.get("identified_risks", [])),
            latency_ms=round((t1 - t0) * 1000, 2),
            model_name=active_model
        )

        # 2. Opposing Counsel Node
        t0 = time.time()
        opposing_res = await opposing_node(state)
        t1 = time.time()
        state.update(opposing_res)
        await token_tracker.log_execution(
            db=db,
            contract_id=contract_id,
            agent_name="Opposing Counsel",
            action="counter_proposal",
            prompt_text=str(state.get("identified_risks", [])),
            completion_text=str(state.get("debate_transcript", [])[-1:]),
            latency_ms=round((t1 - t0) * 1000, 2),
            model_name=active_model
        )

        # 3. Redline Synthesizer Node
        t0 = time.time()
        redline_res = await redline_node(state)
        t1 = time.time()
        state.update(redline_res)
        await token_tracker.log_execution(
            db=db,
            contract_id=contract_id,
            agent_name="Redline Synthesizer",
            action="generate_redlines",
            prompt_text="Synthesize consensus clauses",
            completion_text=str(state.get("redlines", [])),
            latency_ms=round((t1 - t0) * 1000, 2),
            model_name=active_model
        )

        # 4. Obligation Extractor Node
        t0 = time.time()
        obligation_res = await obligation_node(state)
        t1 = time.time()
        state.update(obligation_res)
        await token_tracker.log_execution(
            db=db,
            contract_id=contract_id,
            agent_name="Obligation Agent",
            action="extract_obligations",
            prompt_text="Extract milestones and triggers",
            completion_text=str(state.get("obligations", [])),
            latency_ms=round((t1 - t0) * 1000, 2),
            model_name=active_model
        )

        # Persist results to DB
        stmt = select(Contract).where(Contract.id == contract_id)
        result = await db.execute(stmt)
        contract = result.scalars().first()
        if contract:
            contract.status = "analyzed"
            contract.overall_risk_score = state.get("overall_score", 0.0)
            contract.identified_risks = state.get("identified_risks", [])
            contract.debate_transcript = state.get("debate_transcript", [])
            contract.redlines = state.get("redlines", [])
            contract.obligations = state.get("obligations", [])
            contract.risk_summary = state.get("risk_summary", {})
            await db.commit()
            await db.refresh(contract)

        return state


orchestrator = ContractReviewOrchestrator()
contract_review_graph = orchestrator
