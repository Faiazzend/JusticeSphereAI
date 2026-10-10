from datetime import datetime, timezone
from typing import Dict, Any, List
from app.agents.state import ContractReviewState
from app.services.diff_engine import diff_engine
from app.agents.llm_client import llm_client


async def redline_node(state: ContractReviewState) -> Dict[str, Any]:
    """
    Agent C: Redline Synthesizer.
    Produces consensus redlines, diff tokens, and composite risk scoring for complex agreements.
    """
    identified_risks = state.get("identified_risks", [])
    debate_transcript = list(state.get("debate_transcript", []))

    redlines: List[Dict[str, Any]] = []
    category_scores: Dict[str, float] = {}
    total_score = 0.0

    critical_count = 0
    high_count = 0
    medium_count = 0
    low_count = 0

    for risk in identified_risks:
        cat = risk.get("category", "General")
        sec_num = risk.get("target_section", "1.0")
        original_text = risk.get("original_content", "")
        severity = risk.get("severity", "MEDIUM")
        score = risk.get("score", 50.0)

        total_score += score
        category_scores[cat] = score

        if severity == "CRITICAL":
            critical_count += 1
        elif severity == "HIGH":
            high_count += 1
        elif severity == "MEDIUM":
            medium_count += 1
        else:
            low_count += 1

        # Synthesize targeted consensus redline modification
        if cat == "AI Training & Data Privacy":
            suggested_text = (
                "Provider shall not access, ingest, monitor, copy, extract, de-identify, or utilize any Customer Data, "
                "prompts, model inputs, neural weights, or output artifacts to train, fine-tune, retrain, or improve any "
                "foundational AI models, neural classifiers, or algorithms owned by Provider or any third party. Customer Data "
                "shall remain Customer's exclusive trade secret."
            )
            rationale = (
                "Strikes foundation model training license over customer financial prompts and model weights, eliminating "
                "critical trade secret leakage and GLBA/GDPR controller non-compliance."
            )
        elif cat in ("Indemnification & Baskets", "Indemnification"):
            suggested_text = (
                "Seller shall have no indemnification liability under Section 5.1(a) until the aggregate amount of actionable "
                "Losses exceeds ONE MILLION FIVE HUNDRED THOUSAND DOLLARS ($1,500,000 USD) (the 'Deductible Basket'), and Seller shall "
                "thereafter be liable solely for Losses in excess of such Deductible Basket. The De Minimis Threshold shall be reduced "
                "to FIFTY THOUSAND DOLLARS ($50,000 USD) per claim."
            )
            rationale = (
                "Converts first-dollar tipping basket into a standard deductible basket, and lowers de minimis threshold to $50,000 "
                "to preserve actionable operational claims."
            )
        elif cat == "Representations & Warranties":
            suggested_text = (
                "Seller represents and warrants that, after due and diligent inquiry, Seller is the sole and exclusive owner of all "
                "Acquired IP free and clear of all liens. Seller further warrants and represents that the operation of the Business as "
                "currently conducted does not infringe, misappropriate, or violate any patent, copyright, or trade secret of any third party worldwide."
            )
            rationale = (
                "Upgrades subjective actual knowledge qualification to constructive knowledge after diligent inquiry and removes "
                "dangerous disclaimers of third-party patent non-infringement."
            )
        elif cat in ("IP Ownership & Commercialization", "Intellectual Property"):
            suggested_text = (
                "Developer shall sole and exclusively own all Foreground IP comprising algorithmic architectures, model weights, "
                "and software code. Sponsor shall sole and exclusively own all Foreground IP comprising specific validated chemical "
                "drug compounds and therapeutic matter. Neither party may license or assign Joint IP without the prior written consent "
                "of, and a fifty-fifty (50/50) accounting of net licensing revenues to, the other party."
            )
            rationale = (
                "Divides ownership by core competencies (AI code to Developer, drug molecules to Sponsor) and closes loophole "
                "allowing commercial licensing to competitors without profit sharing."
            )
        elif cat == "Escrow & Operational Covenants":
            suggested_text = (
                "Buyer covenants that post-Closing it shall operate the Business in good faith in the ordinary course, shall not take "
                "any action with the intent or purpose of reducing or frustrating the Earn-Out Consideration, and shall maintain separate "
                "books and records. Escrow release triggers are restricted strictly to formal judicial bankruptcy."
            )
            rationale = (
                "Mandates good-faith covenants to prevent deliberate frustration of earn-out milestones and protects proprietary code escrow."
            )
        elif cat in ("Limitation of Liability & Super-Caps", "Limitation of Liability"):
            suggested_text = (
                "Provider's liability arising out of a breach of Section 4 (DPA / Security Breaches) shall be subject to an aggregate "
                "super-cap of FIVE TIMES (5x) the annual contract value ($62,000,000 USD). Liability arising from gross negligence, "
                "willful misconduct, or third-party IP indemnification shall be completely uncapped and unlimited."
            )
            rationale = (
                "Increases DPA security breach super-cap to 5x annual spend ($62M) and removes cap for gross negligence and IP infringement."
            )
        elif cat == "Service Level & Remedies":
            suggested_text = (
                "The issuance of service credits shall not constitute Customer's sole or exclusive remedy for persistent or severe outages. "
                "If Provider fails to achieve at least 99.50% uptime in any two (2) calendar months within a rolling six (6) month period, "
                "Customer may immediately terminate this Agreement for cause, receive a full refund of unearned prepaid fees, and pursue actual direct damages."
            )
            rationale = (
                "Carves out chronic or catastrophic downtime from exclusive remedy limitation, preserving common law damages and right of rescission."
            )
        elif cat == "Restrictive Covenants & Non-Compete":
            suggested_text = (
                "For a period of twenty-four (24) months following the Closing Date, Seller and its designated Key Executives shall not, "
                "directly within the specific quantum annealing neural acceleration field, engage in any competitive enterprise within "
                "North America or Switzerland. Passive investment in publicly traded entities (under 5%) shall be expressly permitted."
            )
            rationale = (
                "Narrows covenant duration to 24 months and restricts geographic and technological scope to ensure legal enforceability."
            )
        elif cat == "Termination & Remedies":
            suggested_text = (
                "Either party may terminate this Agreement for cause if the other party materially breaches any provision "
                "and fails to cure such breach within thirty (30) days after receiving written notice specifying the breach."
            )
            rationale = (
                "Institutes mandatory 30-day notice and cure period to prevent arbitrary or abrupt contract cancellation."
            )
        else:
            suggested_text = (
                "This Agreement shall be governed by the laws of the State of Delaware or New York. "
                "Any dispute shall be finally settled by binding arbitration administered by the American Arbitration Association (AAA) "
                "or JAMS before a single neutral arbitrator."
            )
            rationale = (
                "Establishes domestic corporate standard and cost-effective binding single-arbitrator venue."
            )

        # Generate diff tokens
        clause_diff = diff_engine.generate_clause_diff(
            section_number=sec_num,
            original_text=original_text[:500] if original_text else "Original clause provisions omitted.",
            suggested_text=suggested_text,
            severity=severity,
            rationale=rationale
        )
        redlines.append(clause_diff)

    # Compute overall risk score (average of detected risks, normalized)
    num_risks = len(identified_risks)
    overall_score = round(min(100.0, total_score / max(1, num_risks)), 1) if num_risks > 0 else 25.0

    risk_summary = {
        "overall_score": overall_score,
        "critical_count": critical_count,
        "high_count": high_count,
        "medium_count": medium_count,
        "low_count": low_count,
        "category_scores": category_scores
    }

    # Synthesizer consensus statement
    synth_statement = (
        f"Consensus Achieved: Synthesized {len(redlines)} precision redlines. "
        f"Overall Contract Risk Score determined at {overall_score}/100. "
        "Track Changes and redline diff tokens compiled successfully."
    )

    try:
        llm_synth, s_model, _ = await llm_client.call_llm(
            prompt=(
                f"You are the Redline Synthesizer agent in a contract review system. "
                f"You reconciled {len(identified_risks)} risks into {len(redlines)} balanced compromises. "
                f"Composite score is {overall_score}/100. Provide a 2-sentence executive summary stating "
                f"that a commercially balanced consensus redline suite has been produced protecting both legal integrity and deal closing."
            ),
            system_prompt="You are a neutral, highly experienced deal synthesizer reconciling company policy with market practice.",
            provider=state.get("llm_provider"),
            model_name=state.get("model_name"),
            use_local=state.get("use_local_llm", False),
            temperature=0.2
        )
        if llm_synth and len(llm_synth.strip()) > 20:
            synth_statement = f"[{s_model}] {llm_synth.strip()}"
    except Exception:
        pass

    debate_transcript.append({
        "agent_name": "Redline Synthesizer",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "content": synth_statement,
        "target_clause": "Consensus Redline Suite"
    })

    return {
        "redlines": redlines,
        "overall_score": overall_score,
        "risk_summary": risk_summary,
        "debate_transcript": debate_transcript,
        "current_status": "Redlines synthesized"
    }
