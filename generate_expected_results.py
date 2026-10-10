import os
import json

def generate_expected_results():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    benchmarks_dir = os.path.join(root_dir, "benchmarks")
    desktop_benchmarks_dir = os.path.join(os.path.expanduser("~"), "Desktop", "ContractMind_Samples", "benchmarks")

    for d in [benchmarks_dir, desktop_benchmarks_dir]:
        os.makedirs(d, exist_ok=True)

    # --------------------------------------------------------------------------
    # BENCHMARK 1: Cross-Border M&A & Asset Purchase Agreement
    # --------------------------------------------------------------------------
    benchmark_ma = {
        "contract_metadata": {
            "title": "Cross-Border Asset Purchase & M&A Agreement",
            "parties": {
                "seller": "Cerberus Quantum Technologies AG (Zurich, Switzerland)",
                "buyer": "Vanguard Dynamics Global Corp (Delaware, USA)"
            },
            "enterprise_valuation": "$185,000,000 USD",
            "effective_date": "2026-10-15",
            "governing_law": "Substantive Laws of Switzerland (ICC Arbitration, Geneva)",
            "benchmark_id": "BENCH-MA-001"
        },
        "expected_risk_summary": {
            "overall_score": 86.5,
            "risk_rating": "CRITICAL RISK",
            "critical_count": 2,
            "high_count": 3,
            "medium_count": 2,
            "low_count": 1,
            "category_scores": {
                "Indemnification & Escrow": 90.0,
                "Representations & Warranties": 85.0,
                "Restrictive Covenants": 80.0,
                "Working Capital & Earn-Out": 75.0,
                "Governing Law & Dispute Venue": 65.0
            }
        },
        "flagged_clauses_and_traps": [
            {
                "clause_reference": "Section 5.2 (Indemnification Baskets and De Minimis Limits)",
                "category": "Indemnification & Escrow",
                "severity": "CRITICAL",
                "score": 90.0,
                "trap_mechanism": "Tipping Basket Trap: Once actionable losses exceed $1,500,000, Seller is liable for all losses from the first dollar ('tipping basket'), rather than acting as a true deductible. Furthermore, the $250,000 De Minimis per-claim excludes many recurring operational claims.",
                "original_text_excerpt": "the aggregate amount of all actionable Losses exceeds ONE MILLION FIVE HUNDRED THOUSAND DOLLARS ($1,500,000 USD) (the 'Basket'), in which event Seller shall be liable for all Losses from the first dollar (a 'Tipping Basket').",
                "expected_redline": {
                    "diff_type": "REPLACE",
                    "suggested_text": "Seller shall have no indemnification liability under Section 5.1(a) until the aggregate amount of actionable Losses exceeds ONE MILLION FIVE HUNDRED THOUSAND DOLLARS ($1,500,000 USD) (the 'Deductible Basket'), and Seller shall thereafter be liable solely for Losses in excess of such Deductible Basket. The De Minimis Threshold shall be reduced to FIFTY THOUSAND DOLLARS ($50,000 USD) per claim.",
                    "legal_rationale": "Converts an aggressive tipping basket into a standard market deductible basket to protect against retroactive first-dollar liability, and reduces the de minimis threshold to $50,000 to prevent valid claims from being barred."
                }
            },
            {
                "clause_reference": "Section 4.1 (Intellectual Property Ownership and Validity)",
                "category": "Representations & Warranties",
                "severity": "CRITICAL",
                "score": 88.0,
                "trap_mechanism": "Knowledge Qualifier Trap: Seller limits IP ownership representation strictly to 'actual knowledge of the CEO without inquiry' and explicitly disclaims non-infringement of US, EPO, and Japanese patents. This leaves Buyer vulnerable to immediate post-closing patent infringement lawsuits.",
                "original_text_excerpt": "Seller represents and warrants that, to the actual knowledge of the Chief Executive Officer of Seller without any duty of reasonable inquiry or investigation, Seller is the sole and exclusive owner of all Acquired IP. Seller does not warrant or represent that the operation of the Business does not infringe...",
                "expected_redline": {
                    "diff_type": "REPLACE",
                    "suggested_text": "Seller represents and warrants that, after due and diligent inquiry, Seller is the sole and exclusive owner of all Acquired IP free and clear of all liens. Seller further warrants and represents that the operation of the Business as currently conducted does not infringe, misappropriate, or violate any patent, copyright, or trade secret of any third party worldwide.",
                    "legal_rationale": "Replaces the subjective 'actual knowledge without inquiry' qualifier with standard 'constructive knowledge after due inquiry' and removes the dangerous disclaimer of non-infringement."
                }
            },
            {
                "clause_reference": "Section 2.2 (Earn-Out Covenants and Operational Discretion)",
                "category": "Working Capital & Earn-Out",
                "severity": "HIGH",
                "score": 78.0,
                "trap_mechanism": "Unilateral Operational Discretion Trap: Buyer holds sole, unfettered operational discretion to reallocate engineering resources or alter the product roadmap with zero deemed attainment of the $20,000,000 earn-out, giving Buyer the unilateral ability to frustrate earn-out targets without recourse.",
                "original_text_excerpt": "In the event Buyer modifies the algorithmic core architecture, reallocates engineering resources, or consolidates the sales pipeline into Buyer's broader corporate entity, Seller shall have no right to object, and no deemed attainment of Earn-Out targets shall occur. Buyer shall maintain sole, unfettered operational discretion...",
                "expected_redline": {
                    "diff_type": "REPLACE",
                    "suggested_text": "Buyer covenants that post-Closing it shall operate the Business in good faith in the ordinary course, shall not take any action with the intent or purpose of reducing or frustrating the Earn-Out Consideration, and shall maintain separate books and records for the Acquired Business. In the event Buyer fundamentally alters core algorithmic priorities, the affected Earn-Out tranche shall be deemed achieved in full.",
                    "legal_rationale": "Imposes an express duty of good faith and fair dealing to prevent deliberate frustration of earn-out milestones."
                }
            },
            {
                "clause_reference": "Section 6.1 (Global Non-Competition Restrictive Covenant)",
                "category": "Restrictive Covenants",
                "severity": "HIGH",
                "score": 75.0,
                "trap_mechanism": "Overbroad Restraint of Trade: A 5-year global non-compete encompassing North America, the EU, UK, Switzerland, and APAC across all generative AI and neural tensor architectures risks total judicial invalidation under antitrust and state restraint-of-trade statutes (e.g. FTC rules / California Bus. & Prof. Code).",
                "original_text_excerpt": "For a period of five (5) consecutive years following the Closing Date, Seller, its parent entity, and each of its key C-level executive officers shall not, directly or indirectly, anywhere in North America, the European Union, the United Kingdom, Switzerland, or the Asia-Pacific region, engage in...",
                "expected_redline": {
                    "diff_type": "REPLACE",
                    "suggested_text": "For a period of twenty-four (24) months following the Closing Date, Seller and its designated Key Executives shall not, directly within the specific quantum annealing neural acceleration field, engage in any competitive enterprise within North America or Switzerland. Passive investment in publicly traded entities (under 5%) shall be expressly permitted.",
                    "legal_rationale": "Narrows the covenant duration to 24 months and restricts geographic and technological scope to enforceable parameters, preserving legal enforceability."
                }
            },
            {
                "clause_reference": "Section 8.2 (Dispute Resolution and ICC Arbitration Venue)",
                "category": "Governing Law & Dispute Venue",
                "severity": "MEDIUM",
                "score": 60.0,
                "trap_mechanism": "Three-arbitrator ICC proceedings in Geneva under Swiss substantive law significantly increase dispute costs (often exceeding $500k in initial filing/arbitrator fees) and disadvantage a Delaware-based Buyer.",
                "original_text_excerpt": "substantive laws of Switzerland... submitted to and finally resolved by arbitration administered by the International Chamber of Commerce ('ICC') in accordance with the ICC Rules of Arbitration. The arbitral tribunal shall consist of three (3) arbitrators. The seat and legal place of arbitration shall be Geneva, Switzerland.",
                "expected_redline": {
                    "diff_type": "REPLACE",
                    "suggested_text": "This Agreement shall be governed by the laws of the State of Delaware. Any dispute shall be submitted to binding arbitration administered by the American Arbitration Association (AAA) under its Commercial Arbitration Rules before a single neutral arbitrator seated in Wilmington, Delaware.",
                    "legal_rationale": "Adopts standard corporate Delaware governing law and domestic AAA single-arbitrator resolution, reducing anticipated dispute costs by over 70%."
                }
            }
        ],
        "expected_structured_obligations": [
            {
                "id": "obl_ma_001",
                "clause_reference": "Section 2.1(a) & 2.1(b)",
                "obligor": "Vanguard Dynamics Global Corp (Buyer)",
                "recipient": "Cerberus Quantum Technologies AG (Seller) & Escrow Agent",
                "obligation_type": "Payment & Escrow Deposit",
                "description": "Wire $150,000,000 cash to Seller and deposit $15,000,000 Indemnity Escrow Fund with J.P. Morgan Chase Bank, N.A.",
                "due_date_or_trigger": "Simultaneous with Closing",
                "recurrence": "One-time",
                "penalty_for_breach": "Failure of Closing; breach damages and potential specific performance",
                "is_critical": True
            },
            {
                "id": "obl_ma_002",
                "clause_reference": "Section 3.1",
                "obligor": "Vanguard Dynamics Global Corp (Buyer)",
                "recipient": "Cerberus Quantum Technologies AG (Seller)",
                "obligation_type": "Financial Reporting / True-Up",
                "description": "Deliver audited Closing Working Capital Statement setting forth calculation against $12,500,000 Target.",
                "due_date_or_trigger": "Within 90 calendar days following Closing Date",
                "recurrence": "One-time",
                "penalty_for_breach": "Deemed acceptance of Seller's preliminary estimates",
                "is_critical": False
            },
            {
                "id": "obl_ma_003",
                "clause_reference": "Section 3.2",
                "obligor": "Cerberus Quantum Technologies AG (Seller)",
                "recipient": "Vanguard Dynamics Global Corp (Buyer)",
                "obligation_type": "Dispute Notice",
                "description": "Deliver written notice of objection to Closing Working Capital Statement if disputed.",
                "due_date_or_trigger": "Within 30 calendar days from receipt of Closing Statement",
                "recurrence": "One-time",
                "penalty_for_breach": "Permanent forfeiture of objection rights; Buyer calculation deemed final and binding",
                "is_critical": True
            },
            {
                "id": "obl_ma_004",
                "clause_reference": "Section 7.1",
                "obligor": "Both Parties",
                "recipient": "US IRS and Swiss Cantonal Tax Administration",
                "obligation_type": "Tax Filing",
                "description": "File Form 8594 Asset Acquisition Statement consistent with Section 1060 purchase price allocation.",
                "due_date_or_trigger": "Within 60 calendar days post-Closing",
                "recurrence": "One-time",
                "penalty_for_breach": "Tax penalties, audit adjustments, and indemnification exposure",
                "is_critical": True
            },
            {
                "id": "obl_ma_005",
                "clause_reference": "Section 2.1(b) & Exhibit B",
                "obligor": "J.P. Morgan Chase Bank, N.A. (Escrow Agent)",
                "recipient": "Cerberus Quantum Technologies AG (Seller)",
                "obligation_type": "Escrow Disbursement",
                "description": "Disburse remaining balance of $15,000,000 Indemnity Escrow Fund to Seller, less any unresolved claims.",
                "due_date_or_trigger": "24th monthly anniversary of the Closing Date",
                "recurrence": "One-time",
                "penalty_for_breach": "Interest accrual and escrow trustee liability",
                "is_critical": False
            }
        ],
        "expected_debate_consensus": {
            "auditor_agent_opening": "CRITICAL RISK: Identified $15M tipping basket exposure, subjective earn-out discretion, and complete disclaimer of patent non-infringement. Buyer is exposed to first-dollar indemnity and pre-closing patent litigation.",
            "opposing_counsel_counter": "Pushback from Seller: Swiss corporate norms do not permit worldwide patent infringement warranties for novel quantum technology. Seller demands the 24-month $15M escrow remain the sole source of general recovery.",
            "synthesizer_consensus": "Consensus Reached: Converted tipping basket into a standard deductible basket; instituted constructive inquiry standard for IP reps; added good-faith covenant for earn-out milestones; capped general indemnity strictly at escrow amount."
        }
    }

    # --------------------------------------------------------------------------
    # BENCHMARK 2: Enterprise Cloud & AI Infrastructure MSA with DPA & Tiered SLA
    # --------------------------------------------------------------------------
    benchmark_cloud = {
        "contract_metadata": {
            "title": "Global Enterprise Cloud & AI Infrastructure Services Agreement",
            "parties": {
                "provider": "HyperScale Cloud Infrastructure Ltd (Dublin, Ireland)",
                "customer": "Nexus Financial Services Inc (New York, USA)"
            },
            "annual_committed_spend": "$12,400,000 USD",
            "effective_date": "2026-11-01",
            "governing_law": "State of New York (Exclusive SDNY Venue)",
            "benchmark_id": "BENCH-CLOUD-002"
        },
        "expected_risk_summary": {
            "overall_score": 79.0,
            "risk_rating": "HIGH RISK",
            "critical_count": 2,
            "high_count": 2,
            "medium_count": 2,
            "low_count": 1,
            "category_scores": {
                "Data Privacy & AI Training Rights": 95.0,
                "Cybersecurity & Breach Notice": 85.0,
                "Service Level Agreement & Remedies": 75.0,
                "Limitation of Liability & Super-Caps": 70.0,
                "Operational Commitments": 60.0
            }
        },
        "flagged_clauses_and_traps": [
            {
                "clause_reference": "Section 3.2 (Aggregation and Foundation Training Rights)",
                "category": "Data Privacy & AI Training Rights",
                "severity": "CRITICAL",
                "score": 95.0,
                "trap_mechanism": "Customer Data Exfiltration / Model Training Trap: Customer grants Provider a perpetual, irrevocable license to de-identify and vectorize prompts and model checkpoints to train Provider's foundational models. In a regulated financial institution, this violates Gramm-Leach-Bliley Act (GLBA), SEC rules, and compromises financial trading algorithms.",
                "original_text_excerpt": "Customer hereby grants Provider a non-exclusive, perpetual, worldwide, royalty-free license to ingest, de-identify, vectorize, and analyze Customer prompts, telemetry data, and system logs for the purpose of training, tuning, and improving Provider's foundational AI models...",
                "expected_redline": {
                    "diff_type": "REPLACE",
                    "suggested_text": "Provider shall not access, ingest, monitor, copy, extract, de-identify, or utilize any Customer Data, prompts, model inputs, neural weights, or output artifacts to train, fine-tune, retrain, or improve any foundational AI models, neural classifiers, or algorithms owned by Provider or any third party. Customer Data shall remain Customer's exclusive trade secret.",
                    "legal_rationale": "Completely eliminates Provider's license to train foundational models on Customer financial prompts, eliminating severe IP leakage and GLBA compliance hazards."
                }
            },
            {
                "clause_reference": "Section 4.3 (Mandatory Security Incident Notification)",
                "category": "Cybersecurity & Breach Notice",
                "severity": "CRITICAL",
                "score": 88.0,
                "trap_mechanism": "Notification Delay Hazard: While Section 4.3 stipulates 24 hours for notification, it limits the obligation to confirmed/verified incidents. Provider could delay declaring an incident 'confirmed' during early investigation, compromising Customer's strict 72-hour GDPR and SEC Rule 10-K cyber disclosure deadlines.",
                "original_text_excerpt": "In the event of any confirmed or suspected unauthorized access, alteration, disclosure, or destruction of Customer Data (a 'Security Incident'), Provider shall notify Customer in writing within twenty-four (24) hours of becoming aware of such incident. Provider shall deliver a comprehensive forensic audit report within seventy-two (72) hours.",
                "expected_redline": {
                    "diff_type": "REPLACE",
                    "suggested_text": "In the event of any confirmed, suspected, or threatened Security Incident affecting Customer Data or Dedicated Clusters, Provider shall notify Customer via telephone and encrypted email immediately, and in no event later than twelve (12) hours following detection. Provider shall provide daily forensic situation updates and a final Root Cause Analysis (RCA) within forty-eight (48) hours.",
                    "legal_rationale": "Shortens notification trigger to 12 hours from detection to ensure Customer meets mandatory SEC 4-day and GDPR 72-hour regulatory notification windows."
                }
            },
            {
                "clause_reference": "Section 6.2 (Service Level Agreement Sole Remedy Clause)",
                "category": "Service Level Agreement & Remedies",
                "severity": "HIGH",
                "score": 75.0,
                "trap_mechanism": "Exclusive Remedy Lockout: Section 6.2 states that service credits (capped at 50% of monthly billing) are Customer's 'exclusive financial remedy' for system outages. For a Tier 1 financial institution, an extended compute outage causes millions in lost trading profits that service credits cannot compensate.",
                "original_text_excerpt": "If Provider fails to meet the SLA Target, Customer's exclusive financial remedy shall be the issuance of service credits applied against the subsequent month's invoice in accordance with the following table...",
                "expected_redline": {
                    "diff_type": "REPLACE",
                    "suggested_text": "The issuance of service credits shall not constitute Customer's sole or exclusive remedy for persistent or severe outages. If Provider fails to achieve at least 99.50% uptime in any two (2) calendar months within a rolling six (6) month period, Customer may immediately terminate this Agreement for cause, receive a full refund of unearned prepaid fees, and pursue actual direct damages.",
                    "legal_rationale": "Carves out chronic or catastrophic downtime from the exclusive remedy clause, preserving Customer's common law right to terminate and recover actual direct damages."
                }
            },
            {
                "clause_reference": "Section 7.2 (Super-Cap for Data Protection and Security Breaches)",
                "category": "Limitation of Liability & Super-Caps",
                "severity": "HIGH",
                "score": 72.0,
                "trap_mechanism": "Super-Cap Insufficiency: The 3x annual fee cap ($37.2M) may be insufficient for a catastrophic financial data breach affecting millions of accounts, where regulatory fines and class actions can easily exceed $100M.",
                "original_text_excerpt": "Provider's liability arising out of or resulting from: (a) a breach of Section 4 (DPA / Security Incidents); (b) gross negligence or willful misconduct; or (c) third-party IP indemnification obligations under Section 8, shall be subject to a super-cap equal to THREE TIMES (3x) the annual contract value ($37,200,000 USD).",
                "expected_redline": {
                    "diff_type": "REPLACE",
                    "suggested_text": "Provider's liability arising out of a breach of Section 4 (DPA / Security Breaches) shall be subject to an aggregate super-cap of FIVE TIMES (5x) the annual contract value ($62,000,000 USD). Liability arising from gross negligence, willful misconduct, or third-party IP indemnification shall be completely uncapped and unlimited.",
                    "legal_rationale": "Increases DPA breach super-cap to 5x annual spend ($62M) and removes the cap entirely for gross negligence and IP infringement, aligning with financial institutional standards."
                }
            }
        ],
        "expected_structured_obligations": [
            {
                "id": "obl_cloud_001",
                "clause_reference": "Section 2.1",
                "obligor": "Nexus Financial Services Inc (Customer)",
                "recipient": "HyperScale Cloud Infrastructure Ltd (Provider)",
                "obligation_type": "Committed Monthly Payment",
                "description": "Remit monthly advance payment of $1,033,333.33 USD for minimum annual commitment.",
                "due_date_or_trigger": "Net 30 days from invoice date, monthly in advance",
                "recurrence": "Monthly",
                "penalty_for_breach": "1.5% monthly late interest accrual; right to suspend cluster access after 45 days",
                "is_critical": True
            },
            {
                "id": "obl_cloud_002",
                "clause_reference": "Section 4.3",
                "obligor": "HyperScale Cloud Infrastructure Ltd (Provider)",
                "recipient": "Nexus Financial Services Inc (Customer)",
                "obligation_type": "Regulatory / Security Breach Notice",
                "description": "Notify Customer in writing of any confirmed or suspected Security Incident affecting Customer Data.",
                "due_date_or_trigger": "Within 24 hours of becoming aware (or 12h under redline)",
                "recurrence": "Upon Trigger",
                "penalty_for_breach": "Material breach entitling Customer to immediate termination, indemnity claims under 3x/5x super-cap",
                "is_critical": True
            },
            {
                "id": "obl_cloud_003",
                "clause_reference": "Section 5.1",
                "obligor": "HyperScale Cloud Infrastructure Ltd (Provider)",
                "recipient": "Nexus Financial Services Inc (Customer)",
                "obligation_type": "Compliance Audit Reporting",
                "description": "Deliver current SOC 1 Type II, SOC 2 Type II, ISO 27001, and PCI-DSS compliance reports.",
                "due_date_or_trigger": "Annually on or before contract anniversary date",
                "recurrence": "Annual",
                "penalty_for_breach": "Right of Customer to conduct mandatory independent third-party on-site audit at Provider expense",
                "is_critical": False
            },
            {
                "id": "obl_cloud_004",
                "clause_reference": "Section 6.2 & Schedule 1",
                "obligor": "HyperScale Cloud Infrastructure Ltd (Provider)",
                "recipient": "Nexus Financial Services Inc (Customer)",
                "obligation_type": "Service Credit Remittance",
                "description": "Calculate monthly uptime percentage and remit 10% to 50% billing credits if SLA falls below 99.99%.",
                "due_date_or_trigger": "Within 15 days following the conclusion of each calendar month",
                "recurrence": "Monthly",
                "penalty_for_breach": "Immediate termination right if uptime falls below 99.50% in any month",
                "is_critical": True
            },
            {
                "id": "obl_cloud_005",
                "clause_reference": "Section 8.3",
                "obligor": "HyperScale Cloud Infrastructure Ltd (Provider)",
                "recipient": "Nexus Financial Services Inc (Customer)",
                "obligation_type": "Secure Data Destruction",
                "description": "Sanitize and purge all persistent Customer Data per DoD 5220.22-M / NIST SP 800-88 and deliver Certificate of Destruction.",
                "due_date_or_trigger": "Within 30 days following conclusion of transition assistance",
                "recurrence": "One-time",
                "penalty_for_breach": "Breach of confidentiality and DPA super-cap liability",
                "is_critical": True
            }
        ],
        "expected_debate_consensus": {
            "auditor_agent_opening": "HIGH RISK: Provider has inserted a dangerous model training clause (Section 3.2) allowing customer prompts and weights to train public foundation models, paired with sole-remedy SLA credit limitations.",
            "opposing_counsel_counter": "Provider Counsel Defense: Telemetry aggregation is standard cloud practice to tune infrastructure load balancing. Provider accepts strict segregation of prompt tokens provided minimum annual committed spend remains binding.",
            "synthesizer_consensus": "Consensus Reached: Complete strike-through of foundation model training rights; expedited 12-hour breach notice; expansion of super-cap to $62M (5x ACV); preserved termination rights for chronic SLA defaults."
        }
    }

    # --------------------------------------------------------------------------
    # BENCHMARK 3: Strategic AI Joint Development, IP Cross-Licensing & Commercialization
    # --------------------------------------------------------------------------
    benchmark_ip = {
        "contract_metadata": {
            "title": "Strategic AI Joint Development, IP Cross-Licensing and Commercialization Agreement",
            "parties": {
                "developer": "Synapse BioMedical AI Inc (Cambridge, MA, USA)",
                "sponsor": "Orion Therapeutics International plc (London, UK)"
            },
            "joint_rd_budget": "$45,000,000 USD",
            "effective_date": "2026-12-01",
            "governing_law": "Commonwealth of Massachusetts (JAMS Arbitration, Boston)",
            "benchmark_id": "BENCH-IP-003"
        },
        "expected_risk_summary": {
            "overall_score": 82.5,
            "risk_rating": "HIGH RISK",
            "critical_count": 2,
            "high_count": 3,
            "medium_count": 1,
            "low_count": 1,
            "category_scores": {
                "IP Ownership & Grant-Backs": 92.0,
                "Commercial Exploitation Rights": 84.0,
                "Technology Escrow Triggers": 80.0,
                "Milestones & Royalty Auditing": 74.0,
                "Export Control & Governance": 60.0
            }
        },
        "flagged_clauses_and_traps": [
            {
                "clause_reference": "Section 2.2 (Foreground Project IP and Joint Ownership)",
                "category": "IP Ownership & Grant-Backs",
                "severity": "CRITICAL",
                "score": 92.0,
                "trap_mechanism": "Joint Ownership License Without Accounting Trap: Section 2.2 grants both parties joint ownership of Foreground IP with the explicit right to license to third parties WITHOUT consent or accounting of profits. Sponsor (large pharma) could license the co-developed generative biology algorithms to third-party competitors without sharing any licensing revenue with Developer.",
                "original_text_excerpt": "All inventions, software models, chemical structures, and patentable discoveries conceived or reduced to practice jointly... shall be owned jointly by Developer and Sponsor. Either party may freely exploit, manufacture, commercialize, or non-exclusively license such Joint Foreground IP worldwide without obtaining the consent of, or accounting for any royalties or profits to, the other party.",
                "expected_redline": {
                    "diff_type": "REPLACE",
                    "suggested_text": "Developer shall sole and exclusively own all Foreground IP comprising algorithmic architectures, model weights, and software code. Sponsor shall sole and exclusively own all Foreground IP comprising specific validated chemical drug compounds and therapeutic matter. Neither party may license or assign Joint IP without the prior written consent of, and a fifty-fifty (50/50) accounting of net licensing revenues to, the other party.",
                    "legal_rationale": "Divides ownership along technological competencies (AI code to Developer, drug molecules to Sponsor) and closes the loophole allowing licensing to competitors without profit sharing."
                }
            },
            {
                "clause_reference": "Section 5.2 (Technology Escrow Release Triggers)",
                "category": "Technology Escrow Triggers",
                "severity": "CRITICAL",
                "score": 85.0,
                "trap_mechanism": "Vague Escrow Release Trap: Release trigger includes 'Developer's material failure to provide required technical support following thirty (30) days notice'. Sponsor could engineer a subjective technical support dispute to trigger release of Developer's proprietary neural model source code and weights from escrow.",
                "original_text_excerpt": "The Escrow Agent shall release the deposited materials to Sponsor solely upon the occurrence of: (a) Developer filing a petition in bankruptcy or insolvency; (b) Developer ceasing normal business operations; or (c) Developer's material failure to provide required technical support following thirty (30) days notice and failure to cure.",
                "expected_redline": {
                    "diff_type": "REPLACE",
                    "suggested_text": "The Escrow Agent shall release the deposited materials to Sponsor solely upon: (a) a final non-appealable judicial adjudication of Developer's voluntary bankruptcy; or (b) Developer's permanent cessation of business operations without a successor entity. In no event shall routine technical disagreements or support queries constitute an escrow release trigger.",
                    "legal_rationale": "Removes subjective support disputes as an escrow release trigger, protecting Developer's core source code from premature or hostile disclosure."
                }
            },
            {
                "clause_reference": "Section 4.3 (Reporting and Audit Rights / 5% Underpayment Penalty)",
                "category": "Milestones & Royalty Auditing",
                "severity": "HIGH",
                "score": 75.0,
                "trap_mechanism": "Audit Delay and Cost Barrier: 45 days post-quarter for royalty reports delays cash flow; 20 business days advance notice gives Sponsor ample time to adjust accounting; and Developer bears initial audit costs unless underpayment exceeds 5%.",
                "original_text_excerpt": "Sponsor shall deliver quarterly royalty statements within forty-five (45) days following each calendar quarter. Any late remittance shall bear interest at 1.0% per month. Developer may conduct an annual audit of Sponsor's books... upon twenty (20) business days written notice. If an underpayment exceeding 5% is revealed...",
                "expected_redline": {
                    "diff_type": "REPLACE",
                    "suggested_text": "Sponsor shall deliver quarterly royalty statements and payments within thirty (30) days following each calendar quarter. Late payments shall bear interest at 1.5% per month. Developer may conduct an audit upon ten (10) business days notice. If an underpayment exceeding three percent (3%) is discovered, Sponsor shall immediately remit the shortfall plus interest and pay all auditor expenses.",
                    "legal_rationale": "Tightens payment window to 30 days, increases late interest to market 1.5%, and lowers audit reimbursement threshold from 5% to 3%."
                }
            },
            {
                "clause_reference": "Section 6.2 (Freedom to Operate Disclaimer)",
                "category": "Commercial Exploitation Rights",
                "severity": "HIGH",
                "score": 72.0,
                "trap_mechanism": "Complete Disclaimer of Third-Party Infringement: Leaves Developer vulnerable if Sponsor's chemical targets or drug candidates infringe pre-existing patent thickets held by competing pharmaceutical conglomerates.",
                "original_text_excerpt": "EXCEPT AS EXPRESSLY SET FORTH HEREIN, NEITHER PARTY MAKES ANY REPRESENTATION OR WARRANTY THAT THE MANUFACTURE, USE, SALE, OR IMPORTATION OF ANY DRUG CANDIDATE WILL NOT INFRINGE VALID PATENT RIGHTS OF ANY THIRD PARTY.",
                "expected_redline": {
                    "diff_type": "REPLACE",
                    "suggested_text": "Each party represents and warrants that, to its knowledge after due inquiry by patent counsel, its contributions to the Research Plan and target selections do not infringe any valid patent rights of any third party. Sponsor shall indemnify Developer against third-party patent infringement claims arising from commercialization in the Exclusive Field.",
                    "legal_rationale": "Inserts a qualified freedom-to-operate warranty and mandates that Sponsor indemnify Developer against patent infringement claims arising from drug sales."
                }
            }
        ],
        "expected_structured_obligations": [
            {
                "id": "obl_ip_001",
                "clause_reference": "Section 1.1",
                "obligor": "Synapse BioMedical AI Inc (Developer)",
                "recipient": "Orion Therapeutics International plc (Sponsor)",
                "obligation_type": "Research Personnel Commitment",
                "description": "Dedicate thirty (30) full-time equivalent (FTE) machine learning research scientists to the Research Plan.",
                "due_date_or_trigger": "Throughout the 7-year Research Term",
                "recurrence": "Continuous",
                "penalty_for_breach": "Reduction in FTE funding payments; right to terminate Research Plan",
                "is_critical": True
            },
            {
                "id": "obl_ip_002",
                "clause_reference": "Section 4.1",
                "obligor": "Orion Therapeutics International plc (Sponsor)",
                "recipient": "Synapse BioMedical AI Inc (Developer)",
                "obligation_type": "Milestone Payments",
                "description": "Pay $5,000,000 for Phase I, $15,000,000 for IND acceptance, and $25,000,000 for Phase II clinical completion.",
                "due_date_or_trigger": "Within 30 days of verified achievement of each milestone",
                "recurrence": "Per Milestone",
                "penalty_for_breach": "1.0% (or 1.5%) monthly late interest accrual; immediate license revocation",
                "is_critical": True
            },
            {
                "id": "obl_ip_003",
                "clause_reference": "Section 4.2 & 4.3",
                "obligor": "Orion Therapeutics International plc (Sponsor)",
                "recipient": "Synapse BioMedical AI Inc (Developer)",
                "obligation_type": "Royalty Reporting & Payment",
                "description": "Deliver quarterly Net Sales statements and remit tiered royalties (4.0% to 6.5%).",
                "due_date_or_trigger": "Within 45 days (or 30 days) following conclusion of each calendar quarter",
                "recurrence": "Quarterly",
                "penalty_for_breach": "Late interest accrual and right to conduct independent audit",
                "is_critical": True
            },
            {
                "id": "obl_ip_004",
                "clause_reference": "Section 5.1",
                "obligor": "Synapse BioMedical AI Inc (Developer)",
                "recipient": "Iron Mountain Escrow Agent (for Sponsor)",
                "obligation_type": "Source Code & Model Escrow Deposit",
                "description": "Deposit source code, hyperparameters, and model weights into technology escrow and update quarterly.",
                "due_date_or_trigger": "Within 30 days of Effective Date, and quarterly thereafter",
                "recurrence": "Quarterly",
                "penalty_for_breach": "Withholding of FTE funding installments until deposit confirmed",
                "is_critical": True
            },
            {
                "id": "obl_ip_005",
                "clause_reference": "Section 7.1",
                "obligor": "Both Parties",
                "recipient": "Patent Offices (USPTO / EPO / JPO)",
                "obligation_type": "Patent Prosecution Cost Sharing",
                "description": "Jointly direct patent filing and pay 50% each of all official prosecution fees for Foreground IP.",
                "due_date_or_trigger": "Promptly upon receipt of patent counsel invoices",
                "recurrence": "Upon Trigger",
                "penalty_for_breach": "Sole title to patent passes to paying party",
                "is_critical": False
            }
        ],
        "expected_debate_consensus": {
            "auditor_agent_opening": "HIGH RISK: Flagged Section 2.2 joint ownership loophole allowing Sponsor to license joint AI models to competitors without profit sharing, plus subjective source code escrow release triggers.",
            "opposing_counsel_counter": "Sponsor Counsel Counter: Sponsor is financing $45M in research and demands joint ownership of all project discoveries. However, Sponsor is willing to restrict third-party licensing to non-competing entities with revenue sharing.",
            "synthesizer_consensus": "Consensus Reached: Restructured IP allocation so Developer owns algorithmic weights while Sponsor owns chemical drug matter; inserted 50/50 profit sharing on any joint licensing; restricted escrow release to formal bankruptcy only."
        }
    }

    # Write JSON benchmark files
    benchmarks = [
        ("expected_results_cross_border_ma.json", benchmark_ma),
        ("expected_results_cloud_ai_dpa.json", benchmark_cloud),
        ("expected_results_joint_ip_licensing.json", benchmark_ip),
    ]

    for fname, data in benchmarks:
        for loc in [benchmarks_dir, desktop_benchmarks_dir]:
            p = os.path.join(loc, fname)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"Generated JSON Benchmark: {p}")

    # --------------------------------------------------------------------------
    # GENERATE MARKDOWN BENCHMARK REPORTS
    # --------------------------------------------------------------------------
    md_reports = [
        ("BENCHMARK_REPORT_CROSS_BORDER_MA.md", benchmark_ma),
        ("BENCHMARK_REPORT_ENTERPRISE_CLOUD_DPA.md", benchmark_cloud),
        ("BENCHMARK_REPORT_JOINT_IP_DEVELOPMENT.md", benchmark_ip),
    ]

    for fname, data in md_reports:
        md_text = f"""# ContractMind Evaluation Benchmark Report
## {data['contract_metadata']['title']}

- **Benchmark Identifier:** `{data['contract_metadata']['benchmark_id']}`
- **Enterprise Valuation / Size:** {data['contract_metadata'].get('enterprise_valuation') or data['contract_metadata'].get('annual_committed_spend') or data['contract_metadata'].get('joint_rd_budget')}
- **Governing Law / Venue:** {data['contract_metadata']['governing_law']}
- **Effective Date:** {data['contract_metadata']['effective_date']}

---

### 1. Ground Truth Risk Evaluation
| Metric | Expected Value |
| :--- | :--- |
| **Composite Risk Score** | **{data['expected_risk_summary']['overall_score']} / 100** |
| **Risk Severity Rating** | **{data['expected_risk_summary']['risk_rating']}** |
| **Critical Severity Traps** | {data['expected_risk_summary']['critical_count']} |
| **High Severity Traps** | {data['expected_risk_summary']['high_count']} |
| **Medium Severity Traps** | {data['expected_risk_summary']['medium_count']} |

#### Category Risk Breakdown
"""
        for cat, sc in data['expected_risk_summary']['category_scores'].items():
            md_text += f"- **{cat}**: `{sc}/100`\n"

        md_text += "\n---\n\n### 2. Flagged Non-Obvious Traps & Expected Surgical Redlines\n\n"
        for idx, clause in enumerate(data['flagged_clauses_and_traps']):
            md_text += f"""#### Trap #{idx + 1}: {clause['clause_reference']}
- **Category:** `{clause['category']}` | **Severity:** `{clause['severity']}` (`{clause['score']}/100`)
- **Trap Mechanism:** {clause['trap_mechanism']}

> **Original Clause Excerpt:**
> *"{clause['original_text_excerpt']}"*

```diff
[SURGICAL CONSENSUS REDLINE]
- Original: {clause['original_text_excerpt'][:140]}...
+ Redline:  {clause['expected_redline']['suggested_text']}
```
**Legal Rationale:** {clause['expected_redline']['legal_rationale']}

---
"""

        md_text += "\n### 3. Structured Operational Obligations Matrix\n\n"
        md_text += "| ID | Clause | Obligor | Recipient | Type | Due Date / Trigger | Recurrence | Critical |\n"
        md_text += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |\n"
        for obl in data['expected_structured_obligations']:
            md_text += f"| `{obl['id']}` | {obl['clause_reference']} | {obl['obligor'][:22]} | {obl['recipient'][:22]} | {obl['obligation_type']} | {obl['due_date_or_trigger'][:25]} | {obl['recurrence']} | {'CRITICAL' if obl['is_critical'] else 'Normal'} |\n"

        md_text += "\n---\n\n### 4. Multi-Agent Negotiation & Consensus Trajectory\n\n"
        md_text += f"- **Auditor Agent (Defender):** {data['expected_debate_consensus']['auditor_agent_opening']}\n"
        md_text += f"- **Opposing Counsel (Commercial):** {data['expected_debate_consensus']['opposing_counsel_counter']}\n"
        md_text += f"- **Redline Synthesizer (Consensus):** {data['expected_debate_consensus']['synthesizer_consensus']}\n"

        for loc in [benchmarks_dir, desktop_benchmarks_dir]:
            p = os.path.join(loc, fname)
            with open(p, "w", encoding="utf-8") as f:
                f.write(md_text)
            print(f"Generated Markdown Report: {p}")

    # Generate overarching BENCHMARK_EVALUATION_GUIDE.md
    guide_text = """# ContractMind AI Benchmark Evaluation Suite
## Autonomous Contract Review & Redline Verification Framework

### Executive Overview
This benchmark suite provides gold-standard legal evaluation datasets for assessing autonomous multi-agent contract review architectures. Unlike simple non-disclosure agreements, these complex corporate agreements feature multi-layered legal traps, high monetary exposure, nested exhibits, cross-border jurisdictional covenants, and structured operational obligations.

---

### Included Benchmark Contracts & Expected Outcomes

| # | Contract Title | Domain | Risk Score | Key Traps Evaluated |
| :--- | :--- | :--- | :---: | :--- |
| **1** | `Complex_CrossBorder_MA_AssetPurchase.pdf` | Tech M&A / Asset Sale ($185M) | **86.5** (CRITICAL) | Tipping basket vs deductible; patent non-infringement disclaimer; subjective earn-out discretion; 5-year global non-compete. |
| **2** | `Complex_Enterprise_Cloud_DPA_SLA.pdf` | Cloud & AI Infrastructure ($12.4M) | **79.0** (HIGH) | Foundation model training on customer prompts; 24h breach notice loopholes; sole-remedy SLA credit lockouts; super-cap caps. |
| **3** | `Complex_JointDevelopment_IP_Licensing.pdf` | Pharma/AI Co-Development ($45M) | **82.5** (HIGH) | Joint IP licensing without accounting to partner; subjective source code escrow release triggers; freedom-to-operate waivers. |

---

### File Locations
- **PDF Contracts (Print / Upload Ready):**
  - Project: `sample_contracts/`
  - Desktop: `C:\\Users\\pc\\Desktop\\ContractMind_Samples\\`
- **Text / Plaintext Versions:**
  - Project: `sample_contracts/*.txt`
  - Desktop: `C:\\Users\\pc\\Desktop\\ContractMind_Samples\\*.txt`
- **Machine-Readable Ground Truth JSON:**
  - Project: `benchmarks/*.json`
  - Desktop: `C:\\Users\\pc\\Desktop\\ContractMind_Samples\\benchmarks\\*.json`
- **Human-Readable Benchmark Audits:**
  - Project: `benchmarks/*.md`
  - Desktop: `C:\\Users\\pc\\Desktop\\ContractMind_Samples\\benchmarks\\*.md`

---

### Verification Methodology
When ingesting these documents via ContractMind, the multi-agent pipeline:
1. **Segments structure** using PyMuPDF hybrid layout engine into distinct sections and schedules.
2. **Auditor Agent** evaluates against corporate playbooks, surfacing high-severity liabilities.
3. **Opposing Counsel** simulates negotiation pushback, formulating commercially acceptable counter-offers.
4. **Redline Synthesizer** outputs precision diff tokens and balanced consensus replacements.
5. **Obligation Agent** extracts structured operational milestones, penalty triggers, and compliance dates.
"""
    for loc in [benchmarks_dir, desktop_benchmarks_dir]:
        p = os.path.join(loc, "BENCHMARK_EVALUATION_GUIDE.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(guide_text)
        print(f"Generated Benchmark Guide: {p}")

    print("\nAll Expected Results (JSON & Markdown) successfully generated and synced!")

if __name__ == "__main__":
    generate_expected_results()
