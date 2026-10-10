import os
import pymupdf

def create_styled_pdf(filename: str, title: str, subtitle: str, sections: list):
    doc = pymupdf.open()
    
    # Page dimensions: standard Letter (612 x 792)
    page_width, page_height = 612, 792
    margin_x = 54
    margin_y = 54
    usable_width = page_width - (2 * margin_x)
    
    current_y = margin_y
    page = doc.new_page(width=page_width, height=page_height)
    
    # Header Banner
    page.insert_text((margin_x, current_y + 15), title, fontsize=16, color=(0.1, 0.15, 0.25))
    current_y += 28
    page.insert_text((margin_x, current_y + 10), subtitle, fontsize=10, color=(0.4, 0.45, 0.55))
    current_y += 25
    
    # Divider line
    page.draw_line((margin_x, current_y), (page_width - margin_x, current_y), color=(0.8, 0.8, 0.8), width=1)
    current_y += 20

    for sec in sections:
        sec_title = sec["title"]
        sec_content = sec["content"]
        
        estimated_height = 40 + (len(sec_content) // 65) * 16
        if current_y + estimated_height > (page_height - margin_y):
            page = doc.new_page(width=page_width, height=page_height)
            current_y = margin_y
        
        # Section Header
        page.insert_text((margin_x, current_y + 12), sec_title, fontsize=11, color=(0.15, 0.2, 0.35))
        current_y += 20
        
        # Section Body textbox
        rect = pymupdf.Rect(margin_x, current_y, margin_x + usable_width, current_y + estimated_height + 25)
        page.insert_textbox(rect, sec_content, fontsize=9.5, color=(0.2, 0.2, 0.2))
        current_y += max(45, (len(sec_content) // 65) * 16 + 20)

    doc.save(filename)
    doc.close()
    print(f"Created: {filename}")


# --------------------------------------------------------------------------
# Sample 1: Enterprise MSA (High Risk)
# --------------------------------------------------------------------------
msa_sections = [
    {
        "title": "SECTION 1. DEFINITIONS AND SCOPE OF SERVICES",
        "content": "This Master Services Agreement ('Agreement') is entered into as of October 1, 2026, by and between Apex Global Solutions Inc. ('Vendor') and Zenith Enterprises LLC ('Client'). Vendor shall provide cloud systems architecture, AI deployment, and enterprise software engineering services as further described in Statements of Work ('SOW') executed under this Agreement."
    },
    {
        "title": "SECTION 2. FEES, INVOICING AND PAYMENT TERMS",
        "content": "Client shall pay all undisputed fees within Net 30 days of receiving Vendor's monthly invoice. Any overdue amounts shall accrue late interest at the rate of 1.5% per month or the highest rate permitted by law. Failure to remit payment within 45 days constitutes material breach entitling Vendor to suspend services."
    },
    {
        "title": "SECTION 3. INTELLECTUAL PROPERTY AND ASSIGNMENT",
        "content": "Vendor hereby irrevocably assigns, transfers, and conveys to Client all right, title, and interest worldwide in and to all Work Product, including all source code, inventions, and pre-existing Background Intellectual Property, algorithmic models, and proprietary tools developed prior to or during the engagement."
    },
    {
        "title": "SECTION 4. INDEMNIFICATION AND DEFENSE",
        "content": "Vendor shall solely defend, indemnify, and hold harmless Client, its parent companies, affiliates, directors, and employees from and against any and all claims, liabilities, damages, losses, costs, and expenses (including legal fees) arising out of or resulting from the performance of the services, third-party intellectual property claims, or any act or omission of Vendor, without monetary cap or limitation."
    },
    {
        "title": "SECTION 5. LIMITATION OF AGGREGATE LIABILITY",
        "content": "Neither party disclaims liability for consequential or punitive damages. Client's liability under this Agreement shall be limited to fees paid, while Vendor's liability shall remain completely uncapped and unlimited with respect to any indemnification, confidentiality breach, or property damage."
    },
    {
        "title": "SECTION 6. CYBERSECURITY AND INSURANCE",
        "content": "Vendor shall maintain Commercial General Liability insurance of not less than $2,000,000 per occurrence and Cyber Liability insurance of $5,000,000 throughout the Term and for a period of two (2) years following termination. Vendor must submit certificates of insurance within 30 days of execution."
    },
    {
        "title": "SECTION 7. TERM AND TERMINATION FOR CONVENIENCE",
        "content": "Client may terminate this Agreement or any applicable SOW at any time without cause or explanation immediately upon written notice, without providing any cure period. Upon termination, Vendor shall immediately refund all prepaid unearned fees."
    },
    {
        "title": "SECTION 8. GOVERNING LAW AND JURISDICTION",
        "content": "This Agreement shall be governed by, and construed in accordance with, the laws of England and Wales, and the parties submit to the exclusive jurisdiction of the Courts of London, United Kingdom."
    }
]

# --------------------------------------------------------------------------
# Sample 2: SaaS Vendor Agreement (Moderate Risk)
# --------------------------------------------------------------------------
saas_sections = [
    {
        "title": "SECTION 1. SUBSCRIPTION GRANT AND USAGE RESTRICTIONS",
        "content": "Provider grants Customer a non-exclusive, non-transferable subscription right to access and use the SaaS Platform during the Subscription Term solely for internal operations. Customer shall not reverse engineer, decompile, or create derivative works from the Platform."
    },
    {
        "title": "SECTION 2. SERVICE LEVEL AGREEMENT (SLA) AND UPTIME",
        "content": "Provider commits to a 99.9% Monthly Uptime Percentage. If Provider fails to meet this SLA, Customer's sole and exclusive remedy shall be service credits equal to 5% of monthly fees for each 1% of downtime, not to exceed 20% of monthly billing."
    },
    {
        "title": "SECTION 3. DATA PRIVACY AND SECURITY COMPLIANCE",
        "content": "Provider shall implement reasonable technical and organizational safeguards in accordance with GDPR and CCPA standards. In the event of a confirmed security incident affecting Customer Data, Provider shall notify Customer within seventy-two (72) hours of verification."
    },
    {
        "title": "SECTION 4. ANNUAL FEES AND AUTO-RENEWAL",
        "content": "Subscriptions automatically renew for successive 12-month periods unless either party provides written notice of non-renewal at least sixty (60) days prior to the expiration of the current Term. Subscription fees shall increase by 7% annually upon renewal."
    },
    {
        "title": "SECTION 5. MUTUAL CONFIDENTIALITY",
        "content": "Each party agrees to safeguard the disclosing party's Confidential Information with the same degree of care it uses for its own confidential assets, but not less than reasonable care. Obligations survive for five (5) years following agreement expiration."
    },
    {
        "title": "SECTION 6. LIMITATION OF LIABILITY",
        "content": "Provider's total aggregate liability arising out of or related to this Agreement shall be capped at the total amount paid by Customer in the three (3) months preceding the incident giving rise to liability, not to exceed $5,000 USD."
    },
    {
        "title": "SECTION 7. AUDIT AND INSPECTION RIGHTS",
        "content": "Provider grants Customer the right to conduct an independent security audit once annually upon thirty (30) business days advance written notice, subject to customary non-disclosure restrictions."
    },
    {
        "title": "SECTION 8. GOVERNING LAW",
        "content": "This Agreement shall be governed by the laws of the State of Delaware, with disputes resolved via binding American Arbitration Association (AAA) arbitration located in Wilmington, Delaware."
    }
]

# --------------------------------------------------------------------------
# Sample 3: Mutual NDA (Standard / Balanced)
# --------------------------------------------------------------------------
nda_sections = [
    {
        "title": "1. PURPOSE AND DEFINITION OF CONFIDENTIAL INFORMATION",
        "content": "The parties wish to explore a potential business relationship ('Purpose'). Confidential Information includes all proprietary technical, financial, and business materials disclosed by either party, whether in writing, orally, or electronically, marked or identified as confidential."
    },
    {
        "title": "2. NON-DISCLOSURE AND STANDARD OF CARE",
        "content": "Each receiving party agrees to hold all Confidential Information in strict confidence and prevent unauthorized disclosure using at least the same degree of care it uses for its own confidential property, but never less than reasonable care."
    },
    {
        "title": "3. PERMITTED DISCLOSURES AND COMPELLED PROCESS",
        "content": "A receiving party may disclose information to its employees and legal advisors who have a strict need-to-know and are bound by confidentiality covenants no less protective than this Agreement. Disclosures required by valid subpoena or legal process are permitted upon prompt prior notice."
    },
    {
        "title": "4. SURVIVAL OF OBLIGATIONS AND RETURN OF MATERIALS",
        "content": "Confidentiality covenants shall survive for three (3) years from the date of disclosure. Upon written request, the receiving party shall certify the destruction or return of all tangible confidential records within fourteen (14) business days."
    },
    {
        "title": "5. REMEDIES AND INJUNCTIVE RELIEF",
        "content": "The parties acknowledge that unauthorized disclosure causes irreparable harm for which monetary damages alone would be inadequate. The disclosing party shall be entitled to seek injunctive relief in addition to all other legal remedies."
    },
    {
        "title": "6. GOVERNING LAW AND VENUE",
        "content": "This Agreement shall be governed by the laws of the State of New York. The parties consent to the jurisdiction of the state and federal courts located in New York County, New York."
    }
]


if __name__ == "__main__":
    out_dir = os.path.join(os.getcwd(), "sample_contracts")
    os.makedirs(out_dir, exist_ok=True)
    
    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop", "ContractMind_Samples")
    os.makedirs(desktop_dir, exist_ok=True)

    samples = [
        ("Sample_Enterprise_MSA.pdf", "MASTER SERVICES AGREEMENT", "High Exposure Risk Benchmark Contract", msa_sections),
        ("Sample_SaaS_Vendor_Agreement.pdf", "SAAS SUBSCRIPTION AGREEMENT", "Cloud Software Vendor Standard Terms", saas_sections),
        ("Sample_Mutual_NDA.pdf", "MUTUAL NON-DISCLOSURE AGREEMENT", "Standard Corporate Confidentiality Agreement", nda_sections),
    ]

    for fname, title, subtitle, secs in samples:
        path_proj = os.path.join(out_dir, fname)
        create_styled_pdf(path_proj, title, subtitle, secs)
        
        path_desktop = os.path.join(desktop_dir, fname)
        create_styled_pdf(path_desktop, title, subtitle, secs)

    print("All sample PDF contracts generated successfully.")
