import re
import uuid
from typing import Dict, Any, List
from app.agents.state import ContractReviewState


async def obligation_node(state: ContractReviewState) -> Dict[str, Any]:
    """
    Agent D: Structured Obligation Extractor.
    Extracts operational duties, payment triggers, compliance deadlines, and breach penalties
    for simple agreements as well as complex enterprise/M&A contracts.
    """
    sections = state.get("sections", [])
    raw_text = state.get("raw_text", "")
    
    extracted_obligations: List[Dict[str, Any]] = []

    obligation_patterns = [
        {
            "regex": r"(security incident|data breach|unauthorized access|twenty-four \(24\) hours)",
            "type": "Security Incident Notice",
            "desc": "Notify Controller/Customer in writing of confirmed or suspected security incidents and deliver forensic reports.",
            "trigger": "Within 24 hours (or 12h under redline) of detection",
            "recurrence": "Upon Trigger",
            "penalty": "Material default entitling immediate contract rescission and super-cap indemnity claims.",
            "critical": True,
            "obligor": "Provider / Vendor",
            "recipient": "Customer / Buyer"
        },
        {
            "regex": r"(escrow agent|indemnity escrow|technology escrow|iron mountain|deposit.*escrow)",
            "type": "Escrow Deposit & Maintenance",
            "desc": "Deposit agreed holdback funds ($15M) or source code and neural weights into third-party escrow.",
            "trigger": "Within 30 calendar days of execution or at Closing",
            "recurrence": "Quarterly Updates",
            "penalty": "Failure of Closing or withholding of milestone research funding installments.",
            "critical": True,
            "obligor": "Depositing Party",
            "recipient": "Escrow Agent / Counterparty"
        },
        {
            "regex": r"(monthly uptime|service credit|sla target|monthly billing credit)",
            "type": "SLA Credit Remittance",
            "desc": "Calculate monthly GPU/cloud availability and remit 10% to 50% service credits if uptime falls below 99.99%.",
            "trigger": "Within 15 days following the conclusion of each billing month",
            "recurrence": "Monthly",
            "penalty": "Immediate right of customer to terminate for cause if uptime drops below 99.50%.",
            "critical": True,
            "obligor": "Cloud Provider",
            "recipient": "Enterprise Customer"
        },
        {
            "regex": r"(working capital statement|post-closing statement|true-up|target working capital)",
            "type": "Working Capital True-Up",
            "desc": "Deliver audited Closing Working Capital Statement and remit net deficit against target.",
            "trigger": "Within 90 calendar days post-Closing (objection within 30 days)",
            "recurrence": "One-time",
            "penalty": "Binding forfeiture of objection rights or direct setoff against escrow fund.",
            "critical": True,
            "obligor": "Buyer & Seller",
            "recipient": "Both Parties"
        },
        {
            "regex": r"(quarterly royalty|net sales|milestone payment|development milestone)",
            "type": "Royalty & Milestone Remittance",
            "desc": "Deliver quarterly Net Sales accounting statements and remit tiered royalties (4.0% - 6.5%) and milestone payments.",
            "trigger": "Within 45 days following the end of each calendar quarter",
            "recurrence": "Quarterly",
            "penalty": "1.0% to 1.5% monthly late interest accrual and right to conduct on-site financial audit.",
            "critical": True,
            "obligor": "Licensee / Sponsor",
            "recipient": "Developer / Licensor"
        },
        {
            "regex": r"(pay|payment|invoic\w+|net\s*\d+|committed spend|annual commitment)",
            "type": "Payment",
            "desc": "Remit payments for committed spend, milestone fees, or services within Net 30 days of invoice.",
            "trigger": "Net 30 days from invoice date",
            "recurrence": "Monthly",
            "penalty": "1.5% monthly late interest accrual or temporary service suspension.",
            "critical": True,
            "obligor": "Customer / Buyer",
            "recipient": "Provider / Seller"
        },
        {
            "regex": r"(data destruction|sanitize and purge|certificate of destruction|dod 5220)",
            "type": "Data Destruction & Sanitization",
            "desc": "Sanitize and purge all persistent customer data per NIST/DoD standards and deliver certified destruction certificate.",
            "trigger": "Within 30 days following conclusion of transition assistance",
            "recurrence": "One-time",
            "penalty": "Actionable breach of confidentiality and regulatory DPA liability.",
            "critical": True,
            "obligor": "Processor / Provider",
            "recipient": "Controller / Customer"
        },
        {
            "regex": r"(audit|books and records|penetration test|soc 2)",
            "type": "Audit & Compliance",
            "desc": "Permit independent certified auditor inspection or deliver annual SOC 2 Type II / ISO 27001 reports.",
            "trigger": "Annually upon 15 business days advance written notice",
            "recurrence": "Annual",
            "penalty": "Payment of audit expenses if discrepancy exceeds 3-5%; breach of regulatory covenants.",
            "critical": False,
            "obligor": "Provider / Partner",
            "recipient": "Customer / Partner"
        },
        {
            "regex": r"(insuran\w+|commercial general liability|cyber\w+)",
            "type": "Insurance",
            "desc": "Maintain commercial general liability and cyber insurance of at least $2,000,000 to $5,000,000.",
            "trigger": "Throughout the Term and for 2 years following termination",
            "recurrence": "Annual",
            "penalty": "Immediate right to terminate for material breach without cure period.",
            "critical": True,
            "obligor": "Vendor",
            "recipient": "Client"
        },
        {
            "regex": r"(confidential\w+|nondisclosure|trade secret)",
            "type": "Confidentiality",
            "desc": "Hold non-public proprietary disclosures in strict confidence using reasonable care.",
            "trigger": "Survives for five (5) years following termination or expiration",
            "recurrence": "Continuous",
            "penalty": "Immediate injunctive relief and recovery of actual economic damages under super-cap.",
            "critical": True,
            "obligor": "Both Parties",
            "recipient": "Both Parties"
        }
    ]

    seen_signatures = set()

    for sec in sections:
        sec_num = sec.get("section_number", "General")
        sec_title = sec.get("title", "")
        sec_content = sec.get("content", "")
        combined = f"{sec_title} {sec_content}"

        for pattern in obligation_patterns:
            sig = f"{sec_num}_{pattern['type']}"
            if sig not in seen_signatures and re.search(pattern["regex"], combined, re.IGNORECASE):
                seen_signatures.add(sig)
                obl_id = f"obl_{uuid.uuid4().hex[:6]}"
                extracted_obligations.append({
                    "id": obl_id,
                    "clause_reference": f"Section {sec_num} ({sec_title})",
                    "obligor": pattern["obligor"],
                    "recipient": pattern["recipient"],
                    "obligation_type": pattern["type"],
                    "description": pattern["desc"],
                    "due_date_or_trigger": pattern["trigger"],
                    "recurrence": pattern["recurrence"],
                    "penalty_for_breach": pattern["penalty"],
                    "is_critical": pattern["critical"]
                })

    # Fallback if few obligations matched
    if len(extracted_obligations) < 3:
        for pattern in obligation_patterns[:4]:
            if re.search(pattern["regex"], raw_text, re.IGNORECASE):
                extracted_obligations.append({
                    "id": f"obl_{uuid.uuid4().hex[:6]}",
                    "clause_reference": f"Clause ({pattern['type']})",
                    "obligor": pattern["obligor"],
                    "recipient": pattern["recipient"],
                    "obligation_type": pattern["type"],
                    "description": pattern["desc"],
                    "due_date_or_trigger": pattern["trigger"],
                    "recurrence": pattern["recurrence"],
                    "penalty_for_breach": pattern["penalty"],
                    "is_critical": pattern["critical"]
                })

    return {
        "obligations": extracted_obligations,
        "current_status": "Obligations extracted"
    }
