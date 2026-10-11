import re
import time
from datetime import datetime, timezone
from typing import Dict, Any, List

from app.agents.state import ContractReviewState
from app.agents.llm_client import llm_client
from app.core.token_tracker import token_tracker
from app.database import AsyncSessionLocal


RISK_CATEGORIES = [
    {
        "category": "AI Training & Data Privacy",
        "severity": "CRITICAL",
        "score": 95.0,
        "pattern": re.compile(
            r"(ingest, de-identify|foundational ai models|prompts|model checkpoints|training, tuning|training data|sub-processor)",
            re.IGNORECASE,
        ),
        "rationale": "Authorizes unilateral extraction of confidential data to train foundational models without customer opt-out or isolation safeguards.",
        "mitigation": "Insert explicit AI data quarantine clause prohibiting training or retention beyond transient inference.",
    },
    {
        "category": "Indemnification & Baskets",
        "severity": "CRITICAL",
        "score": 88.0,
        "pattern": re.compile(
            r"(indemnif\w+|hold harmless|tipping basket|de minimis threshold|basket)",
            re.IGNORECASE,
        ),
        "rationale": "Imposes first-dollar tipping basket exposure and broad indemnification obligations without mutual defense rights.",
        "mitigation": "Convert tipping basket to true deductible threshold and cap aggregate indemnification at fees paid over preceding 12 months.",
    },
    {
        "category": "Representations & Warranties",
        "severity": "CRITICAL",
        "score": 85.0,
        "pattern": re.compile(
            r"(actual knowledge of the chief executive|without any duty of reasonable inquiry|does not warrant.*infringe|freedom to operate)",
            re.IGNORECASE,
        ),
        "rationale": "Severely dilutes counterparty warranties with an unverified actual-knowledge qualifier, waiving inquiry into known IP encumbrances.",
        "mitigation": "Remove executive actual-knowledge limitation; require warranty after reasonable due inquiry of key officers and technical leads.",
    },
    {
        "category": "IP Ownership & Commercialization",
        "severity": "HIGH",
        "score": 82.0,
        "pattern": re.compile(
            r"(jointly by developer and sponsor|without obtaining the consent of, or accounting|grant-back|irrevocably assigns|foreground ip)",
            re.IGNORECASE,
        ),
        "rationale": "Assigns foreground intellectual property without accounting or consent, permitting counterparty to commercialize derived models.",
        "mitigation": "Mandate exclusive client ownership of all foreground IP and customer-specific enhancements; restrict license to internal use.",
    },
    {
        "category": "Escrow & Operational Covenants",
        "severity": "HIGH",
        "score": 78.0,
        "pattern": re.compile(
            r"(earn-out|unfettered operational discretion|escrow release|technology escrow|working capital statement)",
            re.IGNORECASE,
        ),
        "rationale": "Grants unfettered operational discretion during earn-out measurement periods, jeopardizing escrow milestone release conditions.",
        "mitigation": "Subject operational changes to commercially reasonable standards and quarterly third-party audit.",
    },
    {
        "category": "Limitation of Liability & Super-Caps",
        "severity": "HIGH",
        "score": 75.0,
        "pattern": re.compile(
            r"(limitation of liability|aggregate liability|consequential damages|super-cap)",
            re.IGNORECASE,
        ),
        "rationale": "Asymmetrical liability framework creates one-sided exposure while excluding data breach and confidentiality from super-caps.",
        "mitigation": "Establish mutual liability caps with standard carve-outs for gross negligence, willful misconduct, and confidentiality breaches.",
    },
    {
        "category": "Service Level & Remedies",
        "severity": "HIGH",
        "score": 72.0,
        "pattern": re.compile(
            r"(monthly uptime|service level|service credit|exclusive financial remedy|rto|rpo)",
            re.IGNORECASE,
        ),
        "rationale": "Service credits are designated as the sole and exclusive remedy, eliminating termination rights for persistent chronic outages.",
        "mitigation": "Add chronic outage termination trigger (uptime below 95% for 2 consecutive billing cycles) with full prepaid refund.",
    },
    {
        "category": "Restrictive Covenants & Non-Compete",
        "severity": "MEDIUM",
        "score": 65.0,
        "pattern": re.compile(
            r"(non-competition|five \(5\) consecutive years|directly or indirectly, anywhere in|non-solicitation)",
            re.IGNORECASE,
        ),
        "rationale": "Unreasonable five-year global non-competition restraint creates severe anti-trust and enforceability concerns.",
        "mitigation": "Narrow restrictive covenant to 12 months, restricted specifically to direct competitive product lines.",
    },
    {
        "category": "Termination & Remedies",
        "severity": "MEDIUM",
        "score": 55.0,
        "pattern": re.compile(
            r"(termination|cure period|default|immediate termination)",
            re.IGNORECASE,
        ),
        "rationale": "Unilateral immediate termination without customary 30-day notice and cure mechanisms.",
        "mitigation": "Provide standard 30-day written notice and cure period for non-curable material breaches prior to termination.",
    },
    {
        "category": "Governing Law & Dispute Venue",
        "severity": "MEDIUM",
        "score": 50.0,
        "pattern": re.compile(
            r"(substantive laws of switzerland|icc rules of arbitration|geneva, switzerland|courts of london|governing law)",
            re.IGNORECASE,
        ),
        "rationale": "Offshore foreign jurisdiction introduces cross-border enforcement latency and prohibitive arbitration expense.",
        "mitigation": "Designate neutral domestic venue (e.g. State of Delaware) under AAA expedited commercial rules.",
    },
]


async def auditor_node(state: ContractReviewState) -> ContractReviewState:
    """
    Auditor Agent:
    Scans contract sections against the 10 core risk categories,
    computes risk scores, prompts LLM for opening Auditor Statement,
    and logs execution latency and telemetry.
    """
    start_time = time.time()
    sections = state.get("sections", [])
    raw_text = state.get("raw_text", "")
    flagged_risks: List[Dict[str, Any]] = []

    # Map sections by content search
    for cat_spec in RISK_CATEGORIES:
        category = cat_spec["category"]
        pattern = cat_spec["pattern"]
        matched_clause_ref = None
        matched_clause_text = None

        # Search sections first
        for sec in sections:
            content = sec.get("content", "")
            title = sec.get("title", "")
            sec_num = sec.get("section_number", "")
            full_sec_text = f"{title}\n{content}"

            m = pattern.search(full_sec_text)
            if m:
                matched_clause_ref = f"Section {sec_num} ({title})"
                # Extract surrounding window
                start = max(0, m.start() - 60)
                end = min(len(full_sec_text), m.end() + 250)
                matched_clause_text = full_sec_text[start:end].strip()
                break

        # Fallback search across raw text if not found in section blocks
        if not matched_clause_ref:
            m = pattern.search(raw_text)
            if m:
                matched_clause_ref = "Contract Provisions"
                start = max(0, m.start() - 60)
                end = min(len(raw_text), m.end() + 250)
                matched_clause_text = raw_text[start:end].strip()

        if matched_clause_ref and matched_clause_text:
            flagged_risks.append({
                "id": f"risk_{len(flagged_risks) + 1}",
                "category": category,
                "severity": cat_spec["severity"],
                "score": cat_spec["score"],
                "clause_reference": matched_clause_ref,
                "original_text": matched_clause_text,
                "legal_rationale": cat_spec["rationale"],
                "mitigation_strategy": cat_spec["mitigation"],
            })

    # Sort risks by score descending
    flagged_risks.sort(key=lambda r: r["score"], reverse=True)

    # Compute risk summary counts
    risk_summary = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for r in flagged_risks:
        sev = r["severity"].lower()
        if sev in risk_summary:
            risk_summary[sev] += 1

    # Prompt LLM for Auditor opening statement
    top_categories = ", ".join([r["category"] for r in flagged_risks[:3]]) or "general contractual provisions"
    prompt = (
        f"You are the Enterprise Auditor Agent. You have analyzed '{state.get('contract_title')}'. "
        f"You flagged {len(flagged_risks)} high-exposure clauses, primarily in {top_categories}. "
        f"Deliver a sharp opening audit findings statement explaining why these provisions violate enterprise policy."
    )
    system_prompt = (
        "You are an elite Enterprise Auditor and Compliance Counsel. Deliver an authoritative, concise legal audit statement."
    )

    llm_resp, llm_latency, model_used = await llm_client.call_llm(
        prompt=prompt,
        system_prompt=system_prompt,
        provider=state.get("llm_provider"),
        model_name=state.get("model_name"),
        use_local=state.get("use_local_llm", False),
        api_key_override=state.get("api_key_override"),
    )

    total_latency_ms = (time.time() - start_time) * 1000.0

    # Log telemetry
    async with AsyncSessionLocal() as db:
        await token_tracker.log_execution(
            db=db,
            contract_id=state.get("contract_id"),
            agent_name="Auditor Agent",
            action="risk_scan_and_opening_statement",
            prompt_text=prompt,
            completion_text=llm_resp,
            latency_ms=total_latency_ms,
            model_name=model_used,
            details=f"Flagged {len(flagged_risks)} risks",
        )

    transcript_entry = {
        "agent_name": "Auditor Agent",
        "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S UTC"),
        "content": llm_resp,
        "target_clause": "Executive Audit Overview",
    }

    transcript = list(state.get("debate_transcript", []))
    transcript.append(transcript_entry)

    state["identified_risks"] = flagged_risks
    state["risk_summary"] = risk_summary
    state["debate_transcript"] = transcript
    state["current_status"] = "audited"
    return state
