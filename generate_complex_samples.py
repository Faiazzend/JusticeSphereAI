import os
import json
import pymupdf

def create_complex_pdf(filename: str, doc_title: str, doc_subtitle: str, sections: list):
    """
    Renders a multi-page, publication-grade legal contract PDF using PyMuPDF.
    Includes running headers, page footers, section headers, and text boxes.
    """
    doc = pymupdf.open()
    page_width, page_height = 612, 792  # Standard Letter
    margin_x = 54
    margin_top = 54
    margin_bottom = 54
    usable_width = page_width - (2 * margin_x)
    
    current_page = doc.new_page(width=page_width, height=page_height)
    current_y = margin_top

    # Title Banner on first page
    current_page.insert_text((margin_x, current_y + 16), doc_title, fontsize=15, color=(0.08, 0.12, 0.22))
    current_y += 26
    current_page.insert_text((margin_x, current_y + 10), doc_subtitle, fontsize=9.5, color=(0.35, 0.40, 0.50))
    current_y += 22
    current_page.draw_line((margin_x, current_y), (page_width - margin_x, current_y), color=(0.75, 0.80, 0.85), width=1.2)
    current_y += 20

    for sec in sections:
        sec_title = sec.get("title", "")
        sec_content = sec.get("content", "")
        
        # Estimate section title height
        title_height = 24
        # Rough estimation of lines
        lines_estimate = max(1, len(sec_content) // 72)
        body_height = lines_estimate * 14 + 18
        
        # If title + at least 3 lines of body won't fit, jump to next page
        if current_y + title_height + 50 > (page_height - margin_bottom):
            current_page = doc.new_page(width=page_width, height=page_height)
            current_y = margin_top + 20

        # Draw Section Title
        current_page.insert_text((margin_x, current_y + 11), sec_title, fontsize=10.5, color=(0.12, 0.18, 0.32))
        current_y += title_height

        # Text flow with automatic page splitting
        text_remaining = sec_content.strip()
        while text_remaining:
            available_h = (page_height - margin_bottom) - current_y
            if available_h < 40:
                current_page = doc.new_page(width=page_width, height=page_height)
                current_y = margin_top + 20
                available_h = (page_height - margin_bottom) - current_y

            rect = pymupdf.Rect(margin_x, current_y, margin_x + usable_width, page_height - margin_bottom)
            rc = current_page.insert_textbox(rect, text_remaining, fontsize=9, color=(0.15, 0.15, 0.15))
            
            if rc >= 0:
                # Completely fit! Update current_y
                current_y = (page_height - margin_bottom) - rc + 16
                text_remaining = ""
            else:
                # Text did not completely fit on this page, create next page
                # Cut approximate chunk that fits
                chars_that_fit = int((available_h / 14) * 70)
                # Find space boundary
                split_idx = text_remaining.rfind(" ", 0, max(100, chars_that_fit))
                if split_idx == -1 or split_idx < 100:
                    split_idx = chars_that_fit
                
                # Clear and insert just the portion that fits cleanly
                current_page.draw_rect(rect, color=None, fill=(1, 1, 1))  # clear attempt
                part_to_render = text_remaining[:split_idx]
                current_page.insert_textbox(rect, part_to_render, fontsize=9, color=(0.15, 0.15, 0.15))
                text_remaining = text_remaining[split_idx:].strip()
                
                # Open new page
                current_page = doc.new_page(width=page_width, height=page_height)
                current_y = margin_top + 20

    # Apply Running Headers and Footers to all pages
    total_pages = len(doc)
    for idx, page in enumerate(doc):
        # Header (Pages > 0)
        if idx > 0:
            page.insert_text((margin_x, margin_top - 12), doc_title.upper(), fontsize=7.5, color=(0.4, 0.45, 0.5))
            page.insert_text((page_width - margin_x - 140, margin_top - 12), "STRICTLY CONFIDENTIAL - EXECUTION", fontsize=7.5, color=(0.6, 0.2, 0.2))
            page.draw_line((margin_x, margin_top - 5), (page_width - margin_x, margin_top - 5), color=(0.85, 0.85, 0.85), width=0.5)

        # Footer (All pages)
        page.draw_line((margin_x, page_height - margin_bottom + 15), (page_width - margin_x, page_height - margin_bottom + 15), color=(0.85, 0.85, 0.85), width=0.5)
        page.insert_text((margin_x, page_height - margin_bottom + 28), "ContractMind Autonomous Legal Benchmark System", fontsize=7.5, color=(0.5, 0.55, 0.6))
        page.insert_text((page_width - margin_x - 70, page_height - margin_bottom + 28), f"Page {idx + 1} of {total_pages}", fontsize=7.5, color=(0.5, 0.55, 0.6))

    # Save PDF
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc.save(filename)
    doc.close()
    print(f"Generated ({total_pages} pages): {filename}")


# ==============================================================================
# CONTRACT 1: Cross-Border Tech M&A & Asset Purchase Agreement
# ==============================================================================
ma_sections = [
    {
        "title": "RECITALS AND TRANSACTION STRUCTURE",
        "content": (
            "This ASSET PURCHASE AGREEMENT (this 'Agreement'), dated as of October 15, 2026, is entered into by and between "
            "Cerberus Quantum Technologies AG, a Swiss corporation organized under the laws of the Canton of Zurich ('Seller'), "
            "and Vanguard Dynamics Global Corp., a Delaware corporation ('Buyer'). "
            "WHEREAS, Seller owns proprietary quantum algorithmic models, high-performance neural acceleration patents, and "
            "specialized quantum assembly assets (the 'Business'); and WHEREAS, Buyer desires to purchase from Seller, and Seller "
            "desires to sell to Buyer, substantially all the assets, properties, and rights of Seller utilized in the Business, "
            "for a total aggregate enterprise valuation of ONE HUNDRED EIGHTY-FIVE MILLION DOLLARS ($185,000,000 USD), subject to "
            "the strict terms, covenants, representations, warranties, and escrow holdbacks set forth herein."
        )
    },
    {
        "title": "SECTION 1. PURCHASE AND SALE OF ACQUIRED ASSETS",
        "content": (
            "1.1 Acquired Assets. Upon the terms and subject to the conditions of this Agreement, at the Closing, Seller shall sell, "
            "assign, transfer, convey, and deliver to Buyer, and Buyer shall purchase from Seller, all right, title, and interest in "
            "and to all of the following assets of Seller: (a) all registered patents, patent applications, trade secrets, proprietary "
            "source code repositories, training datasets, and model weight checkpoints set forth on Exhibit A; (b) all transferable "
            "customer contracts, enterprise statements of work, and government research grants; and (c) all physical server nodes, "
            "cryogenic cooling units, and high-frequency interconnect hardware located at Seller's Zurich facility. "
            "\n1.2 Excluded Liabilities. Buyer shall not assume, nor shall Buyer be deemed to have assumed, any liabilities, debts, "
            "or obligations of Seller of any nature whatsoever, whether known or unknown, accrued, absolute, contingent, or otherwise, "
            "including without limitation: (i) any employee severance or pension obligations governed by Swiss employment law; "
            "(ii) any pre-closing tax liabilities under Swiss, EU, or US jurisdictions; and (iii) any pending or threatened litigation "
            "claims set forth on Exhibit B."
        )
    },
    {
        "title": "SECTION 2. PURCHASE PRICE, ESCROW HOLDBACK AND EARN-OUT MILESTONES",
        "content": (
            "2.1 Consideration. The aggregate purchase price for the Acquired Assets shall be $185,000,000 USD, payable as follows: "
            "(a) $150,000,000 USD in immediately available cash wired to Seller at Closing; "
            "(b) $15,000,000 USD (the 'Indemnity Escrow Amount') deposited at Closing with J.P. Morgan Chase Bank, N.A. (the 'Escrow Agent') "
            "to secure Seller's indemnification obligations under Section 5 for a period of twenty-four (24) months post-Closing; and "
            "(c) up to $20,000,000 USD in earn-out milestone payments (the 'Earn-Out Consideration'). "
            "\n2.2 Earn-Out Covenants. The Earn-Out Consideration shall be paid in two equal tranches of $10,000,000 USD each, contingent "
            "upon the Acquired Business achieving: (i) Trailing Twelve Month ('TTM') recognized Annual Recurring Revenue ('ARR') of not less "
            "than $75,000,000 USD within eighteen (18) months post-Closing; and (ii) an adjusted EBITDA margin of at least thirty-five percent "
            "(35%). In the event Buyer modifies the algorithmic core architecture, reallocates engineering resources, or consolidates "
            "the sales pipeline into Buyer's broader corporate entity, Seller shall have no right to object, and no deemed attainment of "
            "Earn-Out targets shall occur. Buyer shall maintain sole, unfettered operational discretion over the Business post-Closing."
        )
    },
    {
        "title": "SECTION 3. WORKING CAPITAL ADJUSTMENT AND POST-CLOSING TRUE-UP",
        "content": (
            "3.1 Post-Closing Working Capital Statement. Within ninety (90) calendar days following the Closing Date, Buyer shall prepare "
            "and deliver to Seller a statement setting forth Buyer's calculation of the Closing Working Capital. "
            "\n3.2 Dispute Mechanism. Seller shall have thirty (30) calendar days from receipt of the Closing Statement to deliver written notice "
            "of disagreement. If Seller fails to deliver an objection notice within said 30-day window, Buyer's calculation shall be deemed final, "
            "conclusive, and binding upon all parties. If Seller timely objects and the parties cannot resolve disputed items within thirty (30) "
            "days, the dispute shall be submitted to KPMG Zurich (the 'Independent Accounting Firm') whose determination shall be final. "
            "\n3.3 Payment of Deficit. If the Final Closing Working Capital is less than the Target Working Capital ($12,500,000 USD), Seller "
            "shall, within ten (10) business days following final determination, pay the amount of such deficit directly to Buyer, or Buyer "
            "may, at its sole election, instruct the Escrow Agent to release such deficit amount directly from the Indemnity Escrow Fund."
        )
    },
    {
        "title": "SECTION 4. REPRESENTATIONS AND WARRANTIES OF SELLER",
        "content": (
            "4.1 Intellectual Property Ownership and Validity. Seller represents and warrants that, to the actual knowledge of the Chief "
            "Executive Officer of Seller without any duty of reasonable inquiry or investigation, Seller is the sole and exclusive owner of all "
            "Acquired IP. Seller does not warrant or represent that the operation of the Business does not infringe, misappropriate, or violate "
            "any valid third-party patents or patent claims issued in the United States, Japan, or the European Patent Office. "
            "\n4.2 Regulatory and AI Compliance. Seller represents that its quantum and neural algorithmic models comply in all material "
            "respects with applicable Swiss Federal Data Protection Act regulations. Seller makes no representations or warranties concerning "
            "compliance with the EU Artificial Intelligence Act (Regulation EU 2024/1689), US Executive Orders on Artificial Intelligence, or "
            "export control restrictions under the US Export Administration Regulations ('EAR'). "
            "\n4.3 Financial Statements. The audited balance sheet and income statements of Seller dated as of December 31, 2025 present fairly "
            "in all material respects the financial condition of the Business in accordance with Swiss GAAP FER."
        )
    },
    {
        "title": "SECTION 5. INDEMNIFICATION, BASKETS AND AGGREGATE LIABILITY CAPS",
        "content": (
            "5.1 Indemnification by Seller. Seller shall defend, indemnify, and hold harmless Buyer, its affiliates, directors, officers, "
            "and successors from and against any and all Losses suffered or incurred arising out of or resulting from: (a) any breach of any "
            "representation or warranty made by Seller; (b) any breach of any covenant or agreement by Seller; and (c) any Excluded Liabilities. "
            "\n5.2 Indemnification Baskets and De Minimis Limits. Seller shall have no indemnification liability under Section 5.1(a) unless: "
            "(i) the Losses resulting from an individual claim exceed TWO HUNDRED FIFTY THOUSAND DOLLARS ($250,000 USD) (the 'De Minimis Threshold'), "
            "and any claim below such amount shall not be actionable; and (ii) the aggregate amount of all actionable Losses exceeds ONE MILLION "
            "FIVE HUNDRED THOUSAND DOLLARS ($1,500,000 USD) (the 'Basket'), in which event Seller shall be liable for all Losses from the first "
            "dollar (a 'Tipping Basket'). "
            "\n5.3 Liability Cap. Seller's maximum aggregate indemnification liability for breaches of General Representations shall be strictly "
            "capped at the Indemnity Escrow Amount ($15,000,000 USD); provided, however, that Fundamental Representations (Organization, Authority, "
            "and Tax Liabilities) shall remain uncapped up to the Total Purchase Price ($185,000,000 USD). "
            "\n5.4 Consequential Damages Waiver. IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY CONSEQUENTIAL, INDIRECT, INCIDENTAL, SPECIAL, "
            "OR PUNITIVE DAMAGES, OR FOR ANY LOST PROFITS OR LOSS OF BUSINESS REPUTATION ARISING OUT OF OR IN CONNECTION WITH THIS AGREEMENT."
        )
    },
    {
        "title": "SECTION 6. RESTRICTIVE COVENANTS AND NON-COMPETITION",
        "content": (
            "6.1 Global Non-Competition. For a period of five (5) consecutive years following the Closing Date, Seller, its parent entity, "
            "and each of its key C-level executive officers shall not, directly or indirectly, anywhere in North America, the European Union, "
            "the United Kingdom, Switzerland, or the Asia-Pacific region, engage in, invest in, manage, operate, consult for, or lend assistance "
            "to any enterprise, startup, or venture that develops, markets, or licenses quantum computing architectures, high-performance "
            "neural tensor processors, or generative AI accelerator hardware. "
            "\n6.2 Non-Solicitation of Key Personnel. For a period of thirty-six (36) months post-Closing, Seller shall not solicit, hire, "
            "recruit, or induce any transited engineer, software architect, or researcher employed by Buyer to terminate their employment."
        )
    },
    {
        "title": "SECTION 7. TAX ALLOCATIONS AND REPORTING",
        "content": (
            "7.1 Purchase Price Allocation. Within sixty (60) calendar days after the Closing Date, Buyer shall prepare and deliver to Seller a draft "
            "allocation of the Purchase Price among the Acquired Assets in accordance with Section 1060 of the US Internal Revenue Code of 1986. "
            "The parties agree to report consistently with such allocation on all IRS Forms 8594 and corresponding Swiss tax authority filings. "
            "\n7.2 Transfer Taxes. All sales, use, transfer, stamp, documentary, or value-added taxes ('Transfer Taxes') incurred in connection with "
            "the consummation of the transactions contemplated by this Agreement shall be borne equally fifty percent (50%) by Buyer and fifty "
            "percent (50%) by Seller."
        )
    },
    {
        "title": "SECTION 8. GOVERNING LAW, DISPUTE RESOLUTION AND ICC ARBITRATION",
        "content": (
            "8.1 Governing Law. This Agreement, and all claims or causes of action arising out of or related to this Agreement, shall be governed "
            "by, and enforced in accordance with, the substantive laws of Switzerland, without regard to conflict of laws principles. The United "
            "Nations Convention on Contracts for the International Sale of Goods (CISG) shall not apply. "
            "\n8.2 Binding ICC Arbitration. Any dispute, controversy, or claim arising out of or relating to this Agreement, including the "
            "formation, interpretation, breach, or termination thereof, shall be submitted to and finally resolved by arbitration administered "
            "by the International Chamber of Commerce ('ICC') in accordance with the ICC Rules of Arbitration. The arbitral tribunal shall consist "
            "of three (3) arbitrators. The seat and legal place of arbitration shall be Geneva, Switzerland. The language of the arbitration "
            "proceedings shall be English. The arbitral award shall be final, non-appealable, and enforceable in any court of competent jurisdiction."
        )
    },
    {
        "title": "EXHIBIT A. SCHEDULE OF ACQUIRED PATENTS AND IP ASSETS",
        "content": (
            "1. EP Patent App 2419201.4 - Quantum Annealing Neural Matrix Acceleration Engine\n"
            "2. US Patent 11,849,203 B2 - Cryogenic Low-Noise Qubit Readout and Superconducting Bus Architecture\n"
            "3. Proprietary Model Repository: Cerberus-QNN-V4 (175 Billion Parameter Quantum Transformer Checkpoint)\n"
            "4. 512 Cryogenic Multi-Core Interconnect Interface Nodes located at Technoparkstrasse 1, 8005 Zurich, Switzerland."
        )
    },
    {
        "title": "EXHIBIT B. EXCLUDED LIABILITIES AND ESCROW AGREEMENT SUMMARY",
        "content": (
            "1. Pre-closing tax assessments by the Zurich Cantonal Tax Administration for fiscal years 2023-2025.\n"
            "2. Pending Swiss Federal Labor Tribunal employment severance claim (Case Ref: ZH-LAB-2025-9941).\n"
            "3. Escrow Agreement Terms: Indemnity Escrow Fund of $15,000,000 USD held by J.P. Morgan Chase Bank, N.A., London Branch, "
            "with release of remaining undisbursed funds on the 24th monthly anniversary of Closing, subject to unresolved claims notices."
        )
    }
]


# ==============================================================================
# CONTRACT 2: Enterprise Cloud & AI Infrastructure MSA with DPA & Tiered SLA
# ==============================================================================
cloud_sections = [
    {
        "title": "RECITALS AND MASTER CLOUD INFRASTRUCTURE FRAMEWORK",
        "content": (
            "This ENTERPRISE CLOUD SERVICES AND AI INFRASTRUCTURE AGREEMENT (this 'Agreement'), effective as of November 1, 2026, "
            "is entered into by and between HyperScale Cloud Infrastructure Ltd., a company organized under the laws of Ireland, "
            "with offices at Grand Canal Dock, Dublin 2 ('Provider'), and Nexus Financial Services Inc., a Delaware corporation, with "
            "headquarters at 200 West Street, New York, NY 10282 ('Customer'). "
            "WHEREAS, Provider operates multi-region high-performance cloud data centers equipped with specialized AI acceleration clusters; "
            "and WHEREAS, Customer desires to procure dedicated enterprise GPU compute, private LLM inference pipelines, and secure data storage "
            "for mission-critical financial applications, subject to stringent security, compliance, and service level covenants."
        )
    },
    {
        "title": "SECTION 1. DEDICATED GPU COMPUTE AND INFRASTRUCTURE PROVISIONING",
        "content": (
            "1.1 Provision of Services. Subject to the terms of this Agreement, Provider shall allocate, configure, and maintain for Customer "
            "a dedicated cluster of five hundred twelve (512) NVIDIA H100 SXM5 Tensor Core GPU nodes ('Dedicated Cluster') housed in Provider's "
            "Tier IV certified data centers in Virginia (US-East) and Frankfurt (EU-Central). Provider guarantees private interconnect throughput "
            "of not less than 3.2 Tbps per node with sub-5-microsecond latency. "
            "\n1.2 Scaling and High Availability. Provider shall ensure automated failover between the designated US and EU compute availability "
            "zones. All data transmission between Customer endpoints and Provider clusters shall be secured using TLS 1.3 in-transit and AES-256 "
            "at-rest encryption with Customer-Managed Encryption Keys (CMEK)."
        )
    },
    {
        "title": "SECTION 2. ANNUAL COMMITTED SPEND, INVOICING AND OVERAGE BILLING",
        "content": (
            "2.1 Committed Enterprise Spend. Customer agrees to a minimum committed annual spend of TWELVE MILLION FOUR HUNDRED THOUSAND DOLLARS "
            "($12,400,000 USD) per contract year (the 'Minimum Annual Commitment'), billed in twelve equal monthly installments of $1,033,333.33 USD "
            "payable in advance. "
            "\n2.2 Overage Compute Fees. Any GPU compute hours exceeding the monthly allocation of 374,000 GPU-hours shall be billed at the overage "
            "rate of $4.50 USD per GPU-hour. Overage fees shall be invoiced monthly in arrears. "
            "\n2.3 Payment Terms and Late Interest. Customer shall pay all undisputed invoices within Net thirty (30) days of receipt. Any amount "
            "not paid when due shall accrue interest at the rate of 1.5% per month or the highest rate permitted by applicable law. In the event "
            "Customer fails to cure an overdue payment within forty-five (45) days of written notice, Provider may temporarily suspend cluster access."
        )
    },
    {
        "title": "SECTION 3. MODEL WEIGHTS, PROMPT CONFIDENTIALITY AND DATA OWNERSHIP",
        "content": (
            "3.1 Customer Data Ownership. As between the parties, Customer owns all right, title, and interest in and to Customer Data, including "
            "all financial records, algorithmic prompts, model inputs, proprietary neural model weights, and output artifacts. "
            "\n3.2 Aggregation and Foundation Training Rights (CRITICAL PROVISION). Customer hereby grants Provider a non-exclusive, perpetual, "
            "worldwide, royalty-free license to ingest, de-identify, vectorize, and analyze Customer prompts, telemetry data, and system logs "
            "for the purpose of training, tuning, and improving Provider's foundational AI models, threat detection neural classifiers, and public "
            "cloud infrastructure algorithms; provided that Provider does not disclose Customer's raw un-anonymized financial figures to third parties. "
            "\n3.3 Reverse Engineering Prohibition. Customer shall not reverse engineer, decompile, or extract the underlying hypervisor firmware "
            "or proprietary scheduling algorithms running on Provider's infrastructure."
        )
    },
    {
        "title": "SECTION 4. DATA PROCESSING ADDENDUM (DPA) AND CROSS-BORDER TRANSFERS",
        "content": (
            "4.1 Controller to Processor Relationship. For the purposes of Regulation (EU) 2016/679 ('GDPR') and the California Consumer Privacy "
            "Act ('CCPA'), Customer acts as the Data Controller and Provider acts solely as the Data Processor. Provider shall process Personal "
            "Data strictly in accordance with Customer's documented instructions and the Data Processing Addendum attached as Exhibit B. "
            "\n4.2 Cross-Border Data Transfers. Where Personal Data originating in the European Economic Area is transferred to US data centers, "
            "the Standard Contractual Clauses (SCCs Module 2 - Controller to Processor) adopted by the European Commission shall govern. "
            "\n4.3 Mandatory Security Incident Notification. In the event of any confirmed or suspected unauthorized access, alteration, disclosure, "
            "or destruction of Customer Data (a 'Security Incident'), Provider shall notify Customer in writing within twenty-four (24) hours of "
            "becoming aware of such incident. Provider shall deliver a comprehensive forensic audit report within seventy-two (72) hours. "
            "\n4.4 Sub-Processors. Provider shall provide Customer with at least thirty (30) days prior written notice before engaging any new "
            "sub-processor. Customer shall have the right to object to such appointment within fifteen (15) days; if the parties cannot resolve "
            "the objection, Customer may terminate the affected Service Order without liability or penalty."
        )
    },
    {
        "title": "SECTION 5. CYBERSECURITY AUDIT, PENETRATION TESTING AND REGULATORY ACCESS",
        "content": (
            "5.1 Annual Compliance Certifications. Provider shall maintain and deliver to Customer annually current SOC 1 Type II, SOC 2 Type II, "
            "ISO/IEC 27001:2022, and PCI-DSS Level 1 compliance reports prepared by an independent certified public accounting firm. "
            "\n5.2 Customer Audit and Penetration Rights. Upon fifteen (15) business days prior written notice, Customer (or its designated "
            "independent security auditor) and authorized financial regulators (including the Federal Reserve and the SEC) shall have the right "
            "to inspect Provider's data center facilities, security controls, access logs, and environmental safeguards during normal business hours. "
            "Customer may conduct non-destructive vulnerability assessments and penetration testing once per calendar year."
        )
    },
    {
        "title": "SECTION 6. SERVICE LEVEL AGREEMENT (SLA), UPTIME AND REMEDIES",
        "content": (
            "6.1 Monthly Uptime Commitment. Provider warrants that the Dedicated GPU Cluster and associated networking shall achieve a Monthly "
            "Uptime Percentage of at least 99.99% during each calendar month (the 'SLA Target'). "
            "\n6.2 Tiered Service Credits. If Provider fails to meet the SLA Target, Customer's exclusive financial remedy shall be the issuance "
            "of service credits applied against the subsequent month's invoice in accordance with the following table: "
            "\n- Uptime 99.90% to 99.98%: 10% credit of monthly billing ($103,333 USD) "
            "\n- Uptime 99.50% to 99.89%: 25% credit of monthly billing ($258,333 USD) "
            "\n- Uptime Below 99.50%: 50% credit of monthly billing ($516,666 USD) AND Customer shall have the immediate right to terminate "
            "this Agreement for material cause without any early termination fee. "
            "\n6.3 Disaster Recovery and Business Continuity. In the event of a catastrophic regional outage, Provider guarantees a Recovery Time "
            "Objective (RTO) of not more than two (2) hours, and a Recovery Point Objective (RPO) of not more than fifteen (15) minutes."
        )
    },
    {
        "title": "SECTION 7. LIMITATION OF LIABILITY AND SUPER-CAPS",
        "content": (
            "7.1 General Aggregate Cap. Except as set forth in Section 7.2, each party's maximum cumulative aggregate liability arising out of or "
            "relating to this Agreement shall be limited to the total fees paid by Customer to Provider in the twelve (12) months preceding the "
            "incident giving rise to liability ($12,400,000 USD). "
            "\n7.2 Super-Cap for Data Protection and Security Breaches. Notwithstanding Section 7.1, Provider's liability arising out of or resulting "
            "from: (a) a breach of Section 4 (DPA / Security Incidents); (b) gross negligence or willful misconduct; or (c) third-party IP "
            "indemnification obligations under Section 8, shall be subject to a super-cap equal to THREE TIMES (3x) the annual contract value "
            "($37,200,000 USD). "
            "\n7.3 Consequential Damages Exclusion. Neither party shall be liable for indirect, punitive, or consequential damages; provided, however, "
            "that administrative fines and regulatory penalties levied by supervisory authorities under GDPR resulting from Provider's security "
            "breach shall be deemed direct actionable damages."
        )
    },
    {
        "title": "SECTION 8. TERM, TRANSITION ASSISTANCE AND DATA DESTRUCTION",
        "content": (
            "8.1 Term. The initial term of this Agreement shall commence on November 1, 2026 and continue for thirty-six (36) months, automatically "
            "renewing for successive twelve (12) month periods unless either party gives written notice of non-renewal at least ninety (90) days "
            "prior to expiration. "
            "\n8.2 Transition Services. Upon any expiration or termination of this Agreement, Provider shall provide Customer with up to ninety (90) "
            "days of orderly transition assistance and data export support at Provider's then-current standard professional services rates. "
            "\n8.3 Secure Data Destruction. Within thirty (30) days following conclusion of the transition period, Provider shall securely sanitize "
            "and purge all Customer Data from all persistent storage drives in compliance with DoD 5220.22-M / NIST SP 800-88 standards and deliver "
            "a written Certificate of Destruction signed by an executive officer."
        )
    },
    {
        "title": "SECTION 9. GOVERNING LAW AND JURISDICTION",
        "content": (
            "9.1 Governing Law. This Agreement shall be governed by, and construed in accordance with, the laws of the State of New York, "
            "without regard to conflict of laws principles that would require the application of the laws of any other jurisdiction. "
            "\n9.2 Exclusive Jurisdiction. Each party irrevocably submits to the exclusive personal jurisdiction of the United States District "
            "Court for the Southern District of New York (SDNY), or, if federal jurisdiction is lacking, the Supreme Court of the State of New York, "
            "New York County. Each party waives all objections based on forum non conveniens."
        )
    },
    {
        "title": "SCHEDULE 1. TIERED SLA AVAILABILITY AND SERVICE CREDIT MATRIX",
        "content": (
            "Measurement Metric: Monthly GPU High-Performance Compute Availability\n"
            "Calculation Formula: [(Total Minutes in Month - Unplanned Downtime Minutes) / Total Minutes in Month] * 100\n"
            "- Tier 1 (99.99% - 100%): Full Operational Compliance (0% Penalty Credit)\n"
            "- Tier 2 (99.90% - 99.98%): 10% Monthly Service Credit ($103,333.33 applied to next invoice)\n"
            "- Tier 3 (99.50% - 99.89%): 25% Monthly Service Credit ($258,333.33 applied to next invoice)\n"
            "- Tier 4 (< 99.50%): 50% Monthly Service Credit ($516,666.66) AND Customer immediate right of contract rescission."
        )
    }
]


# ==============================================================================
# CONTRACT 3: AI Joint Development, Cross-Licensing & Commercialization
# ==============================================================================
joint_ip_sections = [
    {
        "title": "RECITALS AND STRATEGIC ALLIANCE FRAMEWORK",
        "content": (
            "This STRATEGIC AI JOINT DEVELOPMENT, IP CROSS-LICENSING AND COMMERCIALIZATION AGREEMENT (this 'Agreement') is executed as of "
            "December 1, 2026, by and between Synapse BioMedical AI Inc., a Delaware corporation with principal laboratories in Cambridge, "
            "Massachusetts ('Developer'), and Orion Therapeutics International plc, a public limited company registered in England and Wales, "
            "with headquarters in London, UK ('Sponsor'). "
            "WHEREAS, Developer possesses proprietary deep learning generative diffusion models for macromolecular biological folding; and "
            "WHEREAS, Sponsor possesses world-class clinical oncology compounds, biochemical validation wet-labs, and global regulatory "
            "distribution networks; and WHEREAS, Developer and Sponsor desire to establish a multi-year collaborative research program to "
            "co-develop de novo oncology drug candidates, with an aggregate joint research budget of FORTY-FIVE MILLION DOLLARS ($45,000,000 USD)."
        )
    },
    {
        "title": "SECTION 1. JOINT DEVELOPMENT PROGRAM AND STEERING COMMITTEE",
        "content": (
            "1.1 Joint Development Program. The parties shall collaborate in good faith to execute the Research Plan outlined in Exhibit A. "
            "Developer shall commit thirty (30) full-time equivalent ('FTE') dedicated machine learning research scientists, and Sponsor shall "
            "fund all agreed FTE expenses at the rate of $450,000 USD per FTE per calendar year. "
            "\n1.2 Joint Steering Committee (JSC). The alliance shall be governed by a Joint Steering Committee composed of three (3) voting "
            "representatives appointed by Developer and three (3) voting representatives appointed by Sponsor. All decisions of the JSC must be "
            "by unanimous consent. In the event of a deadlocked vote lasting more than twenty (20) business days, the dispute shall be escalated "
            "to the Chief Executive Officers of Developer and Sponsor for good faith resolution."
        )
    },
    {
        "title": "SECTION 2. ALLOCATION OF INTELLECTUAL PROPERTY RIGHTS",
        "content": (
            "2.1 Background Intellectual Property. Each party shall retain sole and exclusive ownership of all right, title, and interest in "
            "and to its pre-existing Background IP developed prior to the effective date or outside the scope of this Agreement. Developer retains "
            "exclusive title to its core foundational bio-diffusion neural architecture and training weights. "
            "\n2.2 Foreground Project IP and Joint Ownership (CRITICAL TRAP). All inventions, software models, chemical structures, and patentable "
            "discoveries conceived or reduced to practice jointly by the parties in performance of the Research Plan ('Foreground IP') shall be "
            "owned jointly by Developer and Sponsor. Either party may freely exploit, manufacture, commercialize, or non-exclusively license such "
            "Joint Foreground IP worldwide without obtaining the consent of, or accounting for any royalties or profits to, the other party. "
            "\n2.3 Grant-Back License. Sponsor hereby grants Developer a non-exclusive, perpetual, worldwide, irrevocable license to practice "
            "and incorporate all Improvements made to Developer's Background IP across all non-therapeutic computational applications."
        )
    },
    {
        "title": "SECTION 3. COMMERCIALIZATION LICENSES AND EXCLUSIVE FIELD OF USE",
        "content": (
            "3.1 Sponsor Exclusive Commercial License. Developer hereby grants Sponsor a worldwide, exclusive, royalty-bearing license under "
            "Developer's interest in the Foreground IP to develop, manufacture, obtain regulatory approval for, and commercialize therapeutic "
            "drug candidates solely within the field of human oncology and immuno-therapeutics (the 'Exclusive Field'). "
            "\n3.2 Developer Retained Fields. Developer retains all rights to exploit the Foreground IP, algorithmic frameworks, and screening "
            "software in all fields outside human therapeutics, including agricultural biotechnology, industrial enzyme synthesis, and diagnostic "
            "imaging algorithms."
        )
    },
    {
        "title": "SECTION 4. FINANCIAL MILESTONE PAYMENTS AND TIERED ROYALTIES",
        "content": (
            "4.1 Development Milestone Payments. In consideration of Developer's R&D contributions, Sponsor shall pay Developer the following "
            "non-refundable milestone payments within thirty (30) days of verified achievement: "
            "(a) $5,000,000 USD upon successful in-silico validation and hit-to-lead confirmation of three (3) kinase inhibitor candidates (Phase I); "
            "(b) $15,000,000 USD upon acceptance of the first Investigational New Drug ('IND') application by the US FDA or EMA (Phase II); and "
            "(c) $25,000,000 USD upon completion of successful Phase II human clinical trials. "
            "\n4.2 Net Sales Commercial Royalties. Sponsor shall pay Developer tiered royalties on global annual Net Sales of commercialized "
            "therapeutic products: "
            "(i) 4.0% on portion of annual Net Sales up to $500,000,000 USD; and "
            "(ii) 6.5% on portion of annual Net Sales exceeding $500,000,000 USD. "
            "\n4.3 Reporting and Audit Rights. Sponsor shall deliver quarterly royalty statements within forty-five (45) days following each calendar "
            "quarter. Any late remittance shall bear interest at 1.0% per month. Developer may conduct an annual audit of Sponsor's books and "
            "sales records upon twenty (20) business days written notice. If an underpayment exceeding 5% is revealed, Sponsor shall reimburse "
            "Developer for all reasonable out-of-pocket audit costs."
        )
    },
    {
        "title": "SECTION 5. SOURCE CODE AND TECHNOLOGY ESCROW",
        "content": (
            "5.1 Technology Escrow Deposit. Within thirty (30) days following the Effective Date, Developer shall deposit a copy of all current "
            "source code, algorithmic hyperparameters, training recipes, and model weights into escrow with Iron Mountain Intellectual Property "
            "Management Inc. (the 'Escrow Agent'). Developer shall deposit updated releases on a quarterly basis. "
            "\n5.2 Escrow Release Triggers. The Escrow Agent shall release the deposited materials to Sponsor solely upon the occurrence of: "
            "(a) Developer filing a petition in bankruptcy or insolvency; (b) Developer ceasing normal business operations; or (c) Developer's "
            "material failure to provide required technical support following thirty (30) days notice and failure to cure."
        )
    },
    {
        "title": "SECTION 6. REPRESENTATIONS, WARRANTIES AND FREEDOM TO OPERATE",
        "content": (
            "6.1 Developer IP Representations. Developer represents and warrants that: (a) it possesses all necessary power and authority to "
            "enter into this Agreement; (b) the Background IP is free and clear of all liens and encumbrances; and (c) no portion of the neural "
            "folding algorithms utilizes or embeds open source software subject to viral or copyleft licenses (including GNU GPL, AGPL, or SSPL). "
            "\n6.2 Freedom to Operate Disclaimer. EXCEPT AS EXPRESSLY SET FORTH HEREIN, NEITHER PARTY MAKES ANY REPRESENTATION OR WARRANTY THAT "
            "THE MANUFACTURE, USE, SALE, OR IMPORTATION OF ANY DRUG CANDIDATE WILL NOT INFRINGE VALID PATENT RIGHTS OF ANY THIRD PARTY."
        )
    },
    {
        "title": "SECTION 7. PATENT PROSECUTION AND ENFORCEMENT COVENANTS",
        "content": (
            "7.1 Joint Patent Prosecution. The parties shall jointly direct the filing, prosecution, and maintenance of all patent applications "
            "covering Foreground IP, using mutually agreed patent counsel. All official filing fees and prosecution expenses shall be shared "
            "equally fifty percent (50%) by Developer and fifty percent (50%) by Sponsor. "
            "\n7.2 Enforcement Against Third-Party Infringers. In the event of suspected third-party patent infringement within the Exclusive Field, "
            "Sponsor shall have the first right, but not the obligation, to initiate legal proceedings at its sole expense. If Sponsor recovers "
            "damages or monetary settlements, Sponsor shall retain all recoveries after deducting reasonable litigation expenses, paying Developer "
            "a royalty equivalent on remaining net proceeds."
        )
    },
    {
        "title": "SECTION 8. REGULATORY COMPLIANCE AND EXPORT CONTROL (EAR/ITAR)",
        "content": (
            "8.1 Export Control Regulations. The algorithmic models and biological datasets developed hereunder are subject to US Export "
            "Administration Regulations (15 C.F.R. Parts 730-774) and potentially the International Traffic in Arms Regulations (ITAR). Neither "
            "party shall export, re-export, or transfer any technical data or AI software to restricted entities or embargoed nations without "
            "first obtaining all required US Department of Commerce export licenses. "
            "\n8.2 Dual-Use Biological AI Oversight. The parties agree to establish an internal Bio-Safety Review Board to review all macromolecular "
            "diffusion models to ensure compliance with international biosecurity standards preventing the accidental generation of toxic compounds."
        )
    },
    {
        "title": "SECTION 9. TERM, TERMINATION AND POST-TERMINATION LICENSES",
        "content": (
            "9.1 Term. This Agreement shall commence on December 1, 2026 and continue for an initial research term of seven (7) years, unless "
            "terminated earlier pursuant to this Section 9. "
            "\n9.2 Termination for Cause. Either party may terminate this Agreement upon sixty (60) days written notice if the other party commits "
            "a material breach of its obligations and fails to cure such breach within the 60-day notice period. "
            "\n9.3 Termination for Sponsor Breach. If Developer terminates this Agreement for Sponsor's uncured material breach: (a) all licenses "
            "granted to Sponsor under Section 3 shall immediately terminate; (b) Sponsor shall assign all of its interest in Joint Foreground IP "
            "to Developer; and (c) all unpaid milestone payments for achieved phases shall accelerate and become immediately due."
        )
    },
    {
        "title": "SECTION 10. GOVERNING LAW AND JAMS ARBITRATION",
        "content": (
            "10.1 Governing Law. This Agreement shall be governed by, and construed in accordance with, the laws of the Commonwealth of "
            "Massachusetts, United States, without regard to principles of conflicts of law. "
            "\n10.2 Binding JAMS Arbitration. Any dispute, claim, or controversy arising out of or relating to this Agreement shall be determined "
            "by final and binding arbitration administered by JAMS in Boston, Massachusetts, pursuant to its Comprehensive Arbitration Rules and "
            "Procedures. The arbitration shall be conducted before a panel of three (3) neutral arbitrators with at least ten (10) years experience "
            "in biotechnology and intellectual property law. Judgment upon the award may be entered in any court of competent jurisdiction."
        )
    },
    {
        "title": "EXHIBIT A. RESEARCH PLAN AND MILESTONE ACCEPTANCE CRITERIA",
        "content": (
            "Phase I: Algorithmic Target Discovery & Binding Affinity Prediction (Months 1-18)\n"
            "- Milestone 1.1: Train bio-diffusion model on 10M synthetic peptide conformations.\n"
            "- Milestone 1.2: Identify 3 hit molecules with sub-nanomolar IC50 binding affinity.\n"
            "Phase II: In Vitro Wet-Lab Synthesis and Animal Model Validation (Months 19-42)\n"
            "- Milestone 2.1: Synthesize 500 mg active pharmaceutical ingredient (API).\n"
            "- Milestone 2.2: Achieve 80% tumor regression in xenograft murine models without acute toxicity.\n"
            "Phase III: IND Submission & Clinical Trial Phase I Authorization (Months 43-60)"
        )
    }
]


# ==============================================================================
# MAIN GENERATOR ROUTINE
# ==============================================================================
def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    sample_dir = os.path.join(root_dir, "sample_contracts")
    desktop_sample_dir = os.path.join(os.path.expanduser("~"), "Desktop", "ContractMind_Samples")
    benchmarks_dir = os.path.join(root_dir, "benchmarks")
    desktop_benchmarks_dir = os.path.join(desktop_sample_dir, "benchmarks")

    for d in [sample_dir, desktop_sample_dir, benchmarks_dir, desktop_benchmarks_dir]:
        os.makedirs(d, exist_ok=True)

    contracts_to_generate = [
        {
            "pdf_name": "Complex_CrossBorder_MA_AssetPurchase.pdf",
            "txt_name": "Complex_CrossBorder_MA_AssetPurchase.txt",
            "title": "CROSS-BORDER ASSET PURCHASE & M&A AGREEMENT",
            "subtitle": "Cerberus Quantum Technologies AG & Vanguard Dynamics Global Corp | $185,000,000 USD",
            "sections": ma_sections
        },
        {
            "pdf_name": "Complex_Enterprise_Cloud_DPA_SLA.pdf",
            "txt_name": "Complex_Enterprise_Cloud_DPA_SLA.txt",
            "title": "GLOBAL ENTERPRISE CLOUD & AI INFRASTRUCTURE MSA",
            "subtitle": "HyperScale Cloud Infrastructure Ltd & Nexus Financial Services Inc | $12,400,000 Annual Spend",
            "sections": cloud_sections
        },
        {
            "pdf_name": "Complex_JointDevelopment_IP_Licensing.pdf",
            "txt_name": "Complex_JointDevelopment_IP_Licensing.txt",
            "title": "STRATEGIC AI JOINT DEVELOPMENT & IP LICENSING AGREEMENT",
            "subtitle": "Synapse BioMedical AI Inc & Orion Therapeutics International plc | $45,000,000 R&D Alliance",
            "sections": joint_ip_sections
        }
    ]

    for item in contracts_to_generate:
        # 1. Generate PDF in sample_contracts
        target_pdf_1 = os.path.join(sample_dir, item["pdf_name"])
        create_complex_pdf(target_pdf_1, item["title"], item["subtitle"], item["sections"])

        # 2. Duplicate to Desktop
        target_pdf_2 = os.path.join(desktop_sample_dir, item["pdf_name"])
        create_complex_pdf(target_pdf_2, item["title"], item["subtitle"], item["sections"])

        # 3. Generate raw text files in both locations
        raw_text_content = f"{item['title']}\n{item['subtitle']}\n\n" + "\n\n".join(
            f"=== {s['title']} ===\n{s['content']}" for s in item["sections"]
        )
        for loc in [sample_dir, desktop_sample_dir]:
            txt_path = os.path.join(loc, item["txt_name"])
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(raw_text_content)
            print(f"Generated Text: {txt_path}")

    print("\nAll 3 Complex Contracts successfully generated in both sample_contracts/ and Desktop!")

if __name__ == "__main__":
    main()
