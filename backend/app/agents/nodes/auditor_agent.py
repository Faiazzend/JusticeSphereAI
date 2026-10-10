import re
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List
from app.agents.state import ContractReviewState
from app.agents.llm_client import llm_client


async def auditor_node(state: ContractReviewState) -> Dict[str, Any]:
    """
    Agent A: Internal Auditor / Defender.
    Identifies high-risk clauses, uncapped indemnifications, AI training traps, and playbook deviations.
    """
    sections = state.get("sections", [])
    playbook_rules = state.get("playbook_rules", [])
    raw_text = state.get("raw_text", "")
    use_local = state.get("use_local_llm", False)
    
    identified_risks: List[Dict[str, Any]] = []
    debate_transcript = list(state.get("debate_transcript", []))

    # Comprehensive risk targets across simple & complex legal agreements
    risk_targets = [
        {
            "category": "AI Training & Data Privacy",
            "regex": r"(ingest, de-identify|foundational ai models|prompts|model checkpoints|training, tuning|training data|sub-processor)",
            "severity": "CRITICAL",
            "base_score": 95.0,
            "rationale": "Clause grants counterparty perpetual license to ingest customer prompts and model weights to train foundation models, violating confidentiality and regulatory privacy mandates.",
            "mitigation": "Completely strike foundation model training rights and mandate strict controller data isolation."
        },
        {
            "category": "Indemnification & Baskets",
            "regex": r"(indemnif\w+|hold harmless|tipping basket|de minimis threshold|basket)",
            "severity": "CRITICAL",
            "base_score": 88.0,
            "rationale": "Imposes first-dollar tipping basket or broad unilateral indemnification without reciprocal protections or reasonable liability caps.",
            "mitigation": "Convert tipping basket to true deductible basket, lower de minimis threshold, and cap exposure."
        },
        {
            "category": "Representations & Warranties",
            "regex": r"(actual knowledge of the chief executive|without any duty of reasonable inquiry|does not warrant.*infringe|freedom to operate)",
            "severity": "CRITICAL",
            "base_score": 85.0,
            "rationale": "Subjective actual knowledge qualification without inquiry and explicit disclaimers of patent non-infringement leave client vulnerable to immediate third-party litigation.",
            "mitigation": "Replace with constructive knowledge after diligent inquiry and insert express third-party patent non-infringement warranty."
        },
        {
            "category": "IP Ownership & Commercialization",
            "regex": r"(jointly by developer and sponsor|without obtaining the consent of, or accounting|grant-back|irrevocably assigns|foreground ip)",
            "severity": "HIGH",
            "base_score": 82.0,
            "rationale": "Joint IP ownership without duty of accounting allows counterparty to commercialize proprietary technology to direct competitors with zero profit sharing.",
            "mitigation": "Divide ownership by core competencies (software vs compound) and mandate mutual consent and 50/50 profit accounting."
        },
        {
            "category": "Escrow & Operational Covenants",
            "regex": r"(earn-out|unfettered operational discretion|escrow release|technology escrow|working capital statement)",
            "severity": "HIGH",
            "base_score": 78.0,
            "rationale": "Unilateral operational discretion threatens earn-out attainment; subjective technical support triggers jeopardize proprietary source code escrow.",
            "mitigation": "Institute express good-faith covenants for earn-outs and restrict escrow releases strictly to judicial bankruptcy."
        },
        {
            "category": "Limitation of Liability & Super-Caps",
            "regex": r"(limitation of liability|aggregate liability|consequential damages|super-cap)",
            "severity": "HIGH",
            "base_score": 75.0,
            "rationale": "Aggregate liability cap is insufficient to cover catastrophic data breach or IP damages; lacks appropriate super-caps.",
            "mitigation": "Institute 5x annual value super-cap for data protection/security breaches and uncap gross negligence."
        },
        {
            "category": "Service Level & Remedies",
            "regex": r"(monthly uptime|service level|service credit|exclusive financial remedy|rto|rpo)",
            "severity": "HIGH",
            "base_score": 72.0,
            "rationale": "Service credits are designated as exclusive remedy, locking client out of direct damage recovery for catastrophic multi-hour compute outages.",
            "mitigation": "Carve out chronic or severe downtime (<99.50%) from sole remedy clause to preserve common law termination and damages."
        },
        {
            "category": "Restrictive Covenants & Non-Compete",
            "regex": r"(non-competition|five \(5\) consecutive years|directly or indirectly, anywhere in|non-solicitation)",
            "severity": "MEDIUM",
            "base_score": 65.0,
            "rationale": "Overbroad 5-year global geographic and technological non-compete risks antitrust unenforceability and undue restraint of trade.",
            "mitigation": "Narrow duration to 24 months, specify core market jurisdictions, and allow passive investments."
        },
        {
            "category": "Termination & Remedies",
            "regex": r"(termination|cure period|default|immediate termination)",
            "severity": "MEDIUM",
            "base_score": 55.0,
            "rationale": "Provides inadequate cure window or permits sudden unilateral contract cancellation.",
            "mitigation": "Institute standard 30-day notice and cure period prior to termination for cause."
        },
        {
            "category": "Governing Law & Dispute Venue",
            "regex": r"(substantive laws of switzerland|icc rules of arbitration|geneva, switzerland|courts of london|governing law)",
            "severity": "MEDIUM",
            "base_score": 50.0,
            "rationale": "Distant foreign arbitral seat (e.g. ICC Geneva under Swiss law) exponentially increases dispute resolution expenses.",
            "mitigation": "Align governing law to Delaware or New York with domestic AAA or JAMS arbitration."
        }
    ]

    seen_categories = set()

    for sec in sections:
        sec_num = sec.get("section_number", "General")
        sec_title = sec.get("title", "")
        sec_content = sec.get("content", "")
        combined = f"{sec_title} {sec_content}"

        for target in risk_targets:
            cat_key = f"{sec_num}_{target['category']}"
            if cat_key not in seen_categories and re.search(target["regex"], combined, re.IGNORECASE):
                seen_categories.add(cat_key)
                risk_id = f"risk_{uuid.uuid4().hex[:6]}"
                identified_risks.append({
                    "id": risk_id,
                    "clause_reference": f"Section {sec_num} ({sec_title})",
                    "category": target["category"],
                    "severity": target["severity"],
                    "score": target["base_score"],
                    "rationale": target["rationale"],
                    "suggested_mitigation": target["mitigation"],
                    "target_section": str(sec_num),
                    "original_content": sec_content[:800]
                })

    # Fallback if no sections matched
    if not identified_risks:
        for target in risk_targets[:4]:
            if re.search(target["regex"], raw_text, re.IGNORECASE):
                identified_risks.append({
                    "id": f"risk_{uuid.uuid4().hex[:6]}",
                    "clause_reference": f"Clause: {target['category']}",
                    "category": target["category"],
                    "severity": target["severity"],
                    "score": target["base_score"],
                    "rationale": target["rationale"],
                    "suggested_mitigation": target["mitigation"],
                    "target_section": "1.0",
                    "original_content": raw_text[:500]
                })

    # Generate Auditor Debate Contribution
    top_risk_categories = ", ".join(list(set(r["category"] for r in identified_risks))[:3])
    auditor_statement = (
        f"Auditor Analysis Complete: Flagged {len(identified_risks)} compliance discrepancies and risk traps. "
        f"Critical exposure identified in: {top_risk_categories or 'General Standard Terms'}. "
        f"Recommending immediate defensive redlines to protect company exposure."
    )

    try:
        llm_auditor, model_used, _ = await llm_client.call_llm(
            prompt=(
                f"You are the Lead Contract Risk Auditor. You just reviewed a contract and flagged {len(identified_risks)} risks. "
                f"Key problematic categories: {top_risk_categories}. Provide a sharp 2-sentence opening statement summarizing "
                f"the legal risks and commanding immediate contractual modifications."
            ),
            system_prompt="You are a strict internal corporate auditor defending the enterprise.",
            provider=state.get("llm_provider"),
            model_name=state.get("model_name"),
            use_local=state.get("use_local_llm", False),
            temperature=0.2
        )
        if llm_auditor and len(llm_auditor.strip()) > 20:
            auditor_statement = f"[{model_used}] {llm_auditor.strip()}"
    except Exception:
        pass

    debate_transcript.append({
        "agent_name": "Auditor Agent",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "content": auditor_statement,
        "target_clause": "Contract Global Review"
    })

    return {
        "identified_risks": identified_risks,
        "debate_transcript": debate_transcript,
        "current_status": "Auditor review complete"
    }
