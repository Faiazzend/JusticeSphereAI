import time
from datetime import datetime, timezone
from typing import Dict, Any, List

from app.agents.state import ContractReviewState
from app.services.diff_engine import diff_engine
from app.agents.llm_client import llm_client
from app.core.token_tracker import token_tracker
from app.database import AsyncSessionLocal


CONSENSUS_REPLACEMENTS = {
    "AI Training & Data Privacy": (
        "Provider covenants and agrees that it shall not ingest, de-identify, process, or utilize Customer Data, "
        "Prompts, or Model Outputs to train, fine-tune, retrain, or improve any foundational AI models, weights, or neural "
        "checkpoints, and all customer data processing shall remain strictly isolated in volatile memory during transient runtime."
    ),
    "Indemnification & Baskets": (
        "Indemnifying Party shall defend, indemnify, and hold harmless Indemnified Party from all third-party claims; "
        "provided, however, that indemnification obligations shall be subject to a true deductible threshold of $100,000 "
        "and general indemnification liability shall not exceed the aggregate fees paid in the preceding twelve (12) months."
    ),
    "Representations & Warranties": (
        "To the best knowledge of Seller, after conducting reasonable and diligent inquiry of its executive officers, "
        "engineering directors, and patent counsel, the Software and deliverables do not infringe, misappropriate, or violate "
        "any valid patent, copyright, trademark, or trade secret of any third party."
    ),
    "IP Ownership & Commercialization": (
        "Customer shall exclusively own all right, title, and interest in and to all Foreground Intellectual Property and deliverables. "
        "Developer retains ownership of pre-existing Background IP and hereby grants Customer an irrevocable, perpetual, worldwide, "
        "royalty-free license to use, modify, and distribute such Background IP solely in connection with the deliverables."
    ),
    "Escrow & Operational Covenants": (
        "Developer shall deposit all source code, deployment scripts, and architectural dependencies into an independent technology escrow "
        "agent on a quarterly basis, subject to release verification upon insolvency or uncured material breach."
    ),
    "Limitation of Liability & Super-Caps": (
        "Except for breaches of confidentiality obligations, gross negligence, or indemnification duties, each party's aggregate liability "
        "shall be limited to fees paid under this Agreement during the twelve (12) months preceding the claim, subject to a mutual super-cap "
        "of two times (2.0x) annual contract value for verifiable data protection breaches."
    ),
    "Service Level & Remedies": (
        "Provider guarantees a Monthly Uptime Percentage of 99.9%. In the event uptime falls below 95.0% during any two (2) consecutive "
        "calendar months, Customer may terminate this Agreement immediately for cause and receive a full pro-rata refund of unearned prepaid fees."
    ),
    "Restrictive Covenants & Non-Compete": (
        "The non-solicitation covenants herein shall remain in effect for a period of twelve (12) consecutive months following the effective date "
        "of termination, and shall strictly apply to senior engineering personnel directly assigned to the project."
    ),
    "Termination & Remedies": (
        "Either party may terminate this Agreement upon written notice if the other party breaches any material term and fails to cure such breach "
        "within thirty (30) days following receipt of written notification specifying the breach."
    ),
    "Governing Law & Dispute Venue": (
        "This Agreement shall be governed by and construed in accordance with the substantive laws of the State of Delaware, without regard to "
        "conflict of laws principles. The parties submit to the exclusive jurisdiction of the state and federal courts located in Wilmington, Delaware."
    ),
}


async def redline_node(state: ContractReviewState) -> ContractReviewState:
    """
    Redline Synthesizer Agent:
    Synthesizes balanced consensus text for each flagged risk,
    invokes diff_engine.generate_clause_diff() to generate word-level diff tokens,
    computes composite overall risk score, and generates consensus statement.
    """
    start_time = time.time()
    flagged_risks = state.get("identified_risks", [])
    redlines: List[Dict[str, Any]] = []
    total_score = 0.0

    for idx, risk in enumerate(flagged_risks):
        cat = risk.get("category", "General Clause")
        orig_text = risk.get("original_text", "")
        clause_id = risk.get("clause_reference", f"Section {idx+1}")
        risk_score = risk.get("score", 60.0)
        risk_severity = risk.get("severity", "HIGH")
        total_score += risk_score

        # Select or prompt consensus revised text
        revised_text = CONSENSUS_REPLACEMENTS.get(cat)
        if not revised_text:
            revised_text = (
                f"[REVISED CONSENSUS: Parties agree to modify {cat} to conform with commercial standard practice, "
                f"ensuring mutual protection, reasonable cure periods, and proportionate liability allocation.]"
            )

        # Generate word-level diff tokens
        diff_tokens = diff_engine.generate_clause_diff(orig_text, revised_text)

        redline_obj = {
            "id": f"rl_{idx + 1}",
            "section_number": clause_id,
            "original_text": orig_text,
            "suggested_text": revised_text,
            "diff_type": cat,
            "risk_severity": risk_severity,
            "legal_rationale": risk.get("legal_rationale", "Synthesized consensus clause balancing risk."),
            "diff_tokens": diff_tokens,
            "accepted": None,  # None: Pending, True: Accepted, False: Rejected
            "custom_prompt": None,
            # Aliases for compatibility
            "clause_id": clause_id,
            "category": cat,
            "revised_text": revised_text,
            "consensus_score": round(max(10.0, risk_score * 0.35), 1),
        }
        redlines.append(redline_obj)

    # Composite overall score
    num_risks = len(flagged_risks)
    if num_risks > 0:
        overall_score = round(min(100.0, total_score / max(1, num_risks)), 1)
    else:
        overall_score = 0.0

    # Prompt LLM for consensus synthesizer statement
    prompt = (
        f"You are the Redline Synthesizer Agent. You arbitrated the debate across {num_risks} clauses. "
        f"The composite unmitigated contract risk score was {overall_score}/100. "
        f"Deliver a balanced arbiter consensus summary announcing the synthesis of Word Track Changes redlines."
    )
    system_prompt = (
        "You are an impartial Legal Arbitrator and Redline Synthesizer. Present a professional consensus resolution statement."
    )

    llm_resp, _, model_used = await llm_client.call_llm(
        prompt=prompt,
        system_prompt=system_prompt,
        provider=state.get("llm_provider"),
        model_name=state.get("model_name"),
        use_local=state.get("use_local_llm", False),
        api_key_override=state.get("api_key_override"),
    )

    total_latency_ms = (time.time() - start_time) * 1000.0

    async with AsyncSessionLocal() as db:
        await token_tracker.log_execution(
            db=db,
            contract_id=state.get("contract_id"),
            agent_name="Redline Synthesizer",
            action="consensus_diff_synthesis",
            prompt_text=f"Synthesized redlines for {num_risks} clauses",
            completion_text=llm_resp,
            latency_ms=total_latency_ms,
            model_name=state.get("model_name") or "fallback-simulator",
            details=f"Generated {len(redlines)} Track Changes diffs. Composite score: {overall_score}",
        )

    transcript = list(state.get("debate_transcript", []))
    transcript.append({
        "agent_name": "Redline Synthesizer",
        "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S UTC"),
        "content": llm_resp,
        "target_clause": "Consensus Redline Synthesis",
    })

    state["redlines"] = redlines
    state["overall_score"] = overall_score
    state["debate_transcript"] = transcript
    state["current_status"] = "redlined"
    return state
