import time
from datetime import datetime, timezone
from typing import Dict, Any, List

from app.agents.state import ContractReviewState
from app.agents.llm_client import llm_client
from app.core.token_tracker import token_tracker
from app.database import AsyncSessionLocal


CATEGORY_FALLBACK_REBUTTALS = {
    "AI Training & Data Privacy": (
        "Opposing Counsel: Our client operates high-throughput multi-tenant infrastructure. "
        "De-identified telemetry is an engineering prerequisite for dynamic inference routing and token compression. "
        "We reject a complete prohibition on telemetry, but we will accept an explicit carve-out barring raw customer prompt "
        "retention for model retraining."
    ),
    "Indemnification & Baskets": (
        "Opposing Counsel: First-dollar tipping indemnification reflects commercial risk allocation negotiated in good faith. "
        "However, to facilitate consensus, we propose restructuring the tipping basket into a $250,000 true deductible threshold, "
        "capping general indemnification at 1.0x total contract value."
    ),
    "Representations & Warranties": (
        "Opposing Counsel: Expanding executive knowledge representations without qualifier exposes founders to frivolous third-party assertions. "
        "We agree to qualify the representation by the knowledge of the Chief Technology Officer after reasonable inquiry of lead architects."
    ),
    "IP Ownership & Commercialization": (
        "Opposing Counsel: Core algorithmic pipelines represent pre-existing background intellectual property. "
        "We cannot assign pipeline architectures to the customer. We propose retaining title to background IP while granting customer "
        "an irrevocable, perpetual, royalty-free license to all project deliverables."
    ),
    "Escrow & Operational Covenants": (
        "Opposing Counsel: Unfettered covenants would stifle ongoing product iteration. We agree to quarterly verification of escrow deposit "
        "materials upon objective technical release triggers."
    ),
    "Limitation of Liability & Super-Caps": (
        "Opposing Counsel: Unlimited liability for consequential damages is commercially uninsurable. We propose a mutual 2.0x super-cap "
        "strictly for verifiable direct damages stemming from security incidents."
    ),
    "Service Level & Remedies": (
        "Opposing Counsel: Service credits represent the industry standard remedy. We will agree to a chronic breach clause permitting "
        "termination only if uptime drops below 96% across three consecutive calendar quarters."
    ),
    "Restrictive Covenants & Non-Compete": (
        "Opposing Counsel: Protection of key customer accounts warrants non-solicitation. We will narrow the restriction from five years to 18 months."
    ),
}


async def opposing_node(state: ContractReviewState) -> ContractReviewState:
    """
    Opposing Counsel Agent:
    Reviews top 4 flagged risks, formulates aggressive commercial pushback,
    proposes realistic compromise, and appends debate turns.
    """
    start_time = time.time()
    flagged_risks = state.get("identified_risks", [])[:4]
    transcript = list(state.get("debate_transcript", []))

    if not flagged_risks:
        # Fallback if no risks were flagged
        rebuttal = "Opposing Counsel: Document represents standard commercial market terms. We see no substantive exposure requiring redline."
        transcript.append({
            "agent_name": "Opposing Counsel",
            "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S UTC"),
            "content": rebuttal,
            "target_clause": "Standard Terms",
        })
        state["debate_transcript"] = transcript
        state["current_status"] = "countered"
        return state

    for risk in flagged_risks:
        cat = risk.get("category", "")
        clause_ref = risk.get("clause_reference", "")
        rationale = risk.get("legal_rationale", "")

        prompt = (
            f"You are aggressive Opposing Counsel representing the counterparty. "
            f"The Enterprise Auditor flagged {cat} in {clause_ref} with rationale: '{rationale}'. "
            f"Defend your client's commercial position, push back firmly against the auditor's claim, "
            f"and propose a realistic, commercially viable compromise."
        )
        system_prompt = (
            "You are aggressive Opposing Counsel. Mount a vigorous defense of the counterparty's commercial posture while offering tactical concessions."
        )

        llm_resp, _, model_used = await llm_client.call_llm(
            prompt=prompt,
            system_prompt=system_prompt,
            provider=state.get("llm_provider"),
            model_name=state.get("model_name"),
            use_local=state.get("use_local_llm", False),
            api_key_override=state.get("api_key_override"),
        )

        # Fallback if LLM output was brief/default
        if len(llm_resp) < 60 and cat in CATEGORY_FALLBACK_REBUTTALS:
            llm_resp = CATEGORY_FALLBACK_REBUTTALS[cat]

        transcript.append({
            "agent_name": "Opposing Counsel",
            "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S UTC"),
            "content": llm_resp,
            "target_clause": f"{cat} ({clause_ref})",
        })

    total_latency_ms = (time.time() - start_time) * 1000.0

    async with AsyncSessionLocal() as db:
        await token_tracker.log_execution(
            db=db,
            contract_id=state.get("contract_id"),
            agent_name="Opposing Counsel",
            action="commercial_counter_debate",
            prompt_text=f"Rebutted {len(flagged_risks)} core risks",
            completion_text=transcript[-1]["content"] if transcript else "",
            latency_ms=total_latency_ms,
            model_name=state.get("model_name") or "fallback-simulator",
            details=f"Generated counter-arguments for {len(flagged_risks)} clauses",
        )

    state["debate_transcript"] = transcript
    state["current_status"] = "countered"
    return state
