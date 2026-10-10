from datetime import datetime, timezone
from typing import Dict, Any, List
from app.agents.state import ContractReviewState
from app.agents.llm_client import llm_client


async def opposing_node(state: ContractReviewState) -> Dict[str, Any]:
    """
    Agent B: Opposing Counsel Agent.
    Simulates aggressive counterparty negotiation, pushes back on overly restrictive
    covenants, and offers commercially viable compromises across complex deals.
    Utilizes real LLM generation when available, with deterministic legal fallback.
    """
    identified_risks = state.get("identified_risks", [])
    debate_transcript = list(state.get("debate_transcript", []))
    use_local = state.get("use_local_llm", False)
    provider = state.get("llm_provider")
    model_name = state.get("model_name")

    for risk in identified_risks[:4]:
        cat = risk.get("category", "")
        clause_ref = risk.get("clause_reference", "Clause")
        orig_content = risk.get("original_content", "")[:350]
        rationale = risk.get("rationale", "")

        opposing_response = ""

        # Attempt real LLM generation for nuanced legal counter-arguments
        prompt = (
            f"You are aggressive Opposing Counsel in a commercial contract negotiation.\n"
            f"The Buyer/Customer auditor flagged Section '{clause_ref}' (Category: {cat}) with this critique: '{rationale}'.\n"
            f"Relevant clause excerpt: \"{orig_content}\"\n\n"
            f"In 2-3 concise, legally sophisticated sentences, defend your client's position, push back against the auditor's claim, "
            f"and propose a realistic, commercially viable compromise."
        )

        try:
            llm_text, used_model, _ = await llm_client.call_llm(
                prompt=prompt,
                system_prompt="You are an elite corporate opposing counsel specializing in tech, M&A, and commercial law.",
                provider=provider,
                model_name=model_name,
                use_local=use_local,
                temperature=0.3
            )
            if llm_text and len(llm_text.strip()) > 20:
                opposing_response = f"[{used_model}] {llm_text.strip()}"
        except Exception:
            opposing_response = ""

        # Heuristic fallback if LLM returned empty or offline
        if not opposing_response:
            if cat == "AI Training & Data Privacy":
                opposing_response = (
                    f"Pushback on {clause_ref}: Aggregated telemetry and anonymized training data is standard across "
                    "enterprise cloud providers to optimize GPU scheduler algorithms. However, we will concede strict segregation "
                    "of customer prompt tokens, confidential financial weights, and agree never to train public foundation models on Customer Data."
                )
            elif cat in ("Indemnification & Baskets", "Indemnification"):
                opposing_response = (
                    f"Commercial response on {clause_ref}: While Seller sought first-dollar tipping protection to account for deal "
                    "repricing, we will agree to convert the $1.5M threshold into a standard deductible basket, provided the $15M "
                    "escrow fund represents the sole and exclusive source of recovery for non-fundamental breaches."
                )
            elif cat == "Representations & Warranties":
                opposing_response = (
                    f"Position on {clause_ref}: A worldwide patent non-infringement warranty without knowledge qualifiers creates "
                    "untenable exposure in deep tech and quantum computing patent thickets. We propose a compromise: constructive knowledge "
                    "after reasonable inquiry of our lead patent counsel, coupled with a 50/50 defense cost split."
                )
            elif cat in ("IP Ownership & Commercialization", "Intellectual Property"):
                opposing_response = (
                    f"Counterparty review on {clause_ref}: As the primary financing partner funding $45M in research, we demand co-ownership "
                    "of resulting inventions. However, to resolve deadlock, we will agree that software and model weights belong exclusively to "
                    "Developer, while therapeutic chemical compounds belong to Sponsor, with a 50/50 net profit split on any out-licensing."
                )
            elif cat == "Escrow & Operational Covenants":
                opposing_response = (
                    f"Negotiation on {clause_ref}: We will agree to restrict technology source code escrow release triggers to formal "
                    "insolvency or complete abandonment of technical support, excluding ordinary service request disputes."
                )
            elif cat in ("Limitation of Liability & Super-Caps", "Limitation of Liability"):
                opposing_response = (
                    f"Position on {clause_ref}: A 5x annual contract value super-cap ($62M) for security incidents is acceptable, "
                    "provided third-party regulatory fines are deducted from the aggregate cap calculation."
                )
            elif cat == "Service Level & Remedies":
                opposing_response = (
                    f"Response on {clause_ref}: We agree that chronic downtime below 99.50% in two consecutive months grants Customer "
                    "the right to terminate without penalty, while maintaining service credits as the standard remedy for minor interruptions."
                )
            elif cat == "Restrictive Covenants & Non-Compete":
                opposing_response = (
                    f"Concession on {clause_ref}: We will agree to narrow the non-compete duration from 5 years to 24 months, "
                    "restricted specifically to the quantum annealing field and North American markets."
                )
            else:
                opposing_response = (
                    f"Position on {clause_ref}: We agree to domestic Delaware or Massachusetts governing law with AAA/JAMS arbitration "
                    "to ensure procedural efficiency and minimize dispute costs."
                )

        debate_transcript.append({
            "agent_name": "Opposing Counsel",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "content": opposing_response,
            "target_clause": clause_ref
        })

    return {
        "debate_transcript": debate_transcript,
        "current_status": "Opposing counsel counter-proposals registered"
    }
