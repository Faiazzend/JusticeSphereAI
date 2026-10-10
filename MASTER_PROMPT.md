# 🏛️ ContractMind v1.5 — The Ultimate Master Architecture & Reproduction Prompt (A-Z)

> **Document Version:** 1.5.2  
> **Target Project:** ContractMind v1.5 (Autonomous Multi-Agent Legal AI Studio)  
> **Track:** JusticeSphere_AI — AI Builders Congress 2026  
> **Repository:** [https://github.com/Faiazzend/JusticeSphereAI](https://github.com/Faiazzend/JusticeSphereAI)

---

```markdown
You are an elite Principal AI Systems Architect and Legal Tech Engineer.
Build "ContractMind v1.5" from scratch: an enterprise-grade, autonomous multi-agent legal intelligence platform that ingests commercial contracts, conducts adversarial negotiation debate, synthesizes consensus redlines with authentic Word Track Changes, extracts structured obligation matrices, and empowers lawyers to filter and browse red-lined clauses by risk severity, interactively accept/reject specific clause revisions, and rewrite prompt instructions to regenerate redlines on demand.

Implement the system strictly following the exact architectural specifications, data models, agent graphs, styling design system, and API protocols below.

================================================================================
TABLE OF CONTENTS
================================================================================
1. High-Level Architecture & Technical Stack
2. Directory Structure & File Hierarchy
3. Database Models & Schema Specifications
4. PDF Ingestion, Table Extraction & PII Redaction
5. Contextual RAG & Semantic Chunking Engine
6. Multi-Agent StateGraph Pipeline (4 Agents)
7. Multi-Provider LLM Gateway & Fallback Simulator
8. Word (.docx) OpenXML Track Changes Engine (with Decision Branching)
9. Model Context Protocol (MCP) Server
10. Token & Cost Telemetry Engine
11. Interactive Redline Decisions, AI Prompt Rewriting & Risk-Level Filtering Engine
12. FastAPI REST API & Streaming Endpoints
13. Frontend: Alpine.js & Tailwind Neo-Legal Studio
14. Deployment & Production Orchestration
15. Verification Checklist

================================================================================
1. HIGH-LEVEL ARCHITECTURE & TECHNICAL STACK
================================================================================
- Backend Framework: FastAPI (Python 3.10+) with async endpoints and lifespan database initialization.
- Database: SQLite with async SQLAlchemy 2.0 (aiosqlite). Fallback to /tmp paths if VERCEL=1 is detected.
- Vector Engine: ChromaDB persistent client with automatic fallback to in-memory term-frequency cosine scorer.
- Document Processing: PyMuPDF (fitz) for text and tabular layout extraction, python-docx with custom OpenXML manipulation for Track Changes.
- Agent Architecture: StateGraph pattern with 4 specialized roles:
  1. Auditor Agent (Enterprise defender, compliance auditor)
  2. Opposing Counsel Agent (Counterparty negotiator, aggressive pusher)
  3. Redline Synthesizer Agent (Consensus arbiter, diff builder, composite scorer)
  4. Obligation Extractor Agent (Calendar extractor, role matrix, penalty monitor)
- Interactive Redlining & Risk Triage: Lawyers can filter and browse proposed redlines by risk severity (Critical, High, Medium, Low) and decision state (Accepted, Rejected, Pending), accept or reject individual proposed redlines, or input custom legal prompts/instructions to regenerate specific clauses using real-time LLM synthesis and diff recomputation.
- Protocol: Model Context Protocol (MCP) HTTP/JSON-RPC gateway exposing tools.
- Frontend: Single-Page Application (SPA) built using Alpine.js 3.14, Tailwind CSS, FontAwesome 6, Plus Jakarta Sans, and JetBrains Mono. Zero React build step required for core UI. Includes an interactive 7-step guided rundown tour with high-intensity glowing halo spotlights.
- Deployment: Fully configured for both local 1-click batch execution and Vercel Multi-Service deployment.

================================================================================
2. DIRECTORY STRUCTURE & FILE HIERARCHY
================================================================================
Create the following directory layout:
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── nodes/
│   │   │   │   ├── auditor_agent.py
│   │   │   │   ├── opposing_agent.py
│   │   │   │   ├── redline_agent.py
│   │   │   │   └── obligation_agent.py
│   │   │   ├── graph.py
│   │   │   ├── llm_client.py
│   │   │   └── state.py
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── analysis.py
│   │   │   │   ├── contracts.py
│   │   │   │   ├── playbook.py
│   │   │   │   └── stream.py
│   │   │   └── deps.py
│   │   ├── core/
│   │   │   ├── pii_redactor.py
│   │   │   ├── security.py
│   │   │   └── token_tracker.py
│   │   ├── mcp_server/
│   │   │   └── server.py
│   │   ├── models/
│   │   │   ├── audit.py
│   │   │   ├── contract.py
│   │   │   └── user.py
│   │   ├── schemas/
│   │   │   ├── contract_schemas.py
│   │   │   ├── obligation_schemas.py
│   │   │   ├── playbook_schemas.py
│   │   │   └── risk_schemas.py
│   │   ├── services/
│   │   │   ├── diff_engine.py
│   │   │   ├── export_service.py
│   │   │   ├── pdf_processor.py
│   │   │   └── rag_engine.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── static/
│   │   └── index.html
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   └── route.ts
│   ├── public/
│   │   └── index.html
│   ├── next.config.js
│   └── package.json
├── sample_contracts/
├── launch.py
├── run_contractmind.bat
├── vercel.json
├── MASTER_PROMPT.md
└── README.md

================================================================================
3. DATABASE MODELS & SCHEMA SPECIFICATIONS
================================================================================
Implement async SQLAlchemy 2.0 models:

1. Contract (`app/models/contract.py`):
   - `id`: String (UUID primary key)
   - `title`: String(255)
   - `original_filename`: String(255)
   - `file_path`: String(512)
   - `status`: String(50), default "uploaded" ("uploaded", "processing", "analyzed", "error")
   - `overall_risk_score`: Float, default 0.0 (0-100 scale)
   - `raw_text`: Text
   - `playbook_name`: String(100), default "Standard Corporate Playbook"
   - `extracted_sections`: JSON (list of {section_number, title, content, page_number})
   - `identified_risks`: JSON (list of risks)
   - `debate_transcript`: JSON (list of {agent_name, timestamp, content, target_clause})
   - `redlines`: JSON (list of clause diff objects containing {id, section_number, original_text, suggested_text, diff_type, risk_severity, legal_rationale, diff_tokens, accepted, custom_prompt})
   - `obligations`: JSON (list of extracted obligation dictionaries)
   - `risk_summary`: JSON (counts of critical, high, medium, low risks)
   - `created_at`: DateTime(timezone=True), default lambda: datetime.now(timezone.utc)
   - `updated_at`: DateTime(timezone=True), onupdate lambda: datetime.now(timezone.utc)

2. AuditLog (`app/models/audit.py`):
   - `id`: Integer primary key, autoincrement
   - `contract_id`: String(36), nullable foreign key
   - `agent_name`: String(100)
   - `action`: String(100)
   - `prompt_tokens`: Integer
   - `completion_tokens`: Integer
   - `total_tokens`: Integer
   - `latency_ms`: Float
   - `model_name`: String(100)
   - `estimated_cost_usd`: Float (6 decimal places)
   - `details`: Text, nullable
   - `created_at`: DateTime(timezone=True), default lambda: datetime.now(timezone.utc)

================================================================================
4. PDF INGESTION, TABLE EXTRACTION & PII REDACTION
================================================================================
1. `app/core/pii_redactor.py`:
   - Define compiled regex patterns for:
     - SSN: `\b\d{3}-\d{2}-\d{4}\b`
     - Credit Cards: `\b(?:\d{4}[-\s]?){3}\d{4}\b`
     - Email: `\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b`
     - Phone: `\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b`
     - Bank Account: `\b\d{8,17}\b`
     - Tax ID: `\b\d{2}-\d{7}\b`
   - Method `redact(text: str) -> Tuple[str, Dict[str, int]]`:
     Replaces matches with `[REDACTED_{TYPE}]` and returns statistics.

2. `app/services/pdf_processor.py`:
   - Open PDF with `fitz.open(file_path)`.
   - Iterate through pages:
     - Extract text with `page.get_text("text")`.
     - Detect tables via `page.find_tables()`. Convert any detected table matrix into clean Markdown format:
       `[TABLE EXHIBIT - Page {p}]\n| col1 | col2 |\n| --- | --- |\n| val1 | val2 |`
     - Concatenate full document text.
   - Run PII redaction on full text.
   - Segment sections via regular expression:
     `r"(?:\n|^)(?:SECTION|ARTICLE|CLAUSE)?\s*(\d+(?:\.\d+)*|[IVXLCDM]+)[\.\:\-\s]+([A-Z][A-Za-z0-9\s\,\-\&\/\(\)]+)(?=\n)"`
   - Fall back to paragraph blocks if no structured numbered headers match.
   - Return `(full_raw_text, list_of_sections)`.

================================================================================
5. CONTEXTUAL RAG & SEMANTIC CHUNKING ENGINE
================================================================================
`app/services/rag_engine.py`:
- Contextual Semantic Chunking:
  For each section in the contract, if length > 1500 chars, break into logical paragraphs.
  Prepend a situational contextual header to every chunk:
  ```
  [Document: {contract_title} | Section: {sec_num} ({title}) | Page: {page}]
  Context: This excerpt defines terms and legal obligations governing {title.lower()}.
  ```
- Storage:
  - Initialize ChromaDB `PersistentClient(path=settings.CHROMA_PERSIST_DIR)`.
  - Upsert chunks into a collection named `f"contract_{contract_id.replace('-', '_')}"`.
  - Maintain an internal in-memory dictionary cache `self._memory_store[contract_id] = chunks`.
  - On `query(contract_id, query_text, n_results=4)`:
    - Attempt ChromaDB vector query.
    - If ChromaDB fails or is unavailable, run token-frequency relevance scoring over `self._memory_store` and return top chunks.
  - Implement `delete_contract(contract_id)` to purge collections from ChromaDB and memory.

================================================================================
6. MULTI-AGENT STATEGRAPH PIPELINE (4 AGENTS)
================================================================================
`app/agents/state.py`:
Define `ContractReviewState(TypedDict)` with:
- `contract_id`: str
- `contract_title`: str
- `raw_text`: str
- `sections`: List[Dict]
- `playbook_rules`: List[Dict]
- `debate_cycle`: int
- `max_debate_cycles`: int
- `use_local_llm`: bool
- `llm_provider`: Optional[str]
- `model_name`: Optional[str]
- `api_key_override`: Optional[str]
- `identified_risks`: List[Dict]
- `debate_transcript`: List[Dict]
- `redlines`: List[Dict]
- `obligations`: List[Dict]
- `risk_summary`: Dict
- `overall_score`: float
- `current_status`: str
- `error`: Optional[str]

`app/agents/graph.py` Orchestrator:
Executes sequentially:
1. `auditor_node`:
   - Scans sections against 10 risk categories with regex signatures, severity, base score, legal rationale, and suggested mitigation:
     1. "AI Training & Data Privacy" (CRITICAL, 95.0) -> regex: `(ingest, de-identify|foundational ai models|prompts|model checkpoints|training, tuning|training data|sub-processor)`
     2. "Indemnification & Baskets" (CRITICAL, 88.0) -> regex: `(indemnif\w+|hold harmless|tipping basket|de minimis threshold|basket)`
     3. "Representations & Warranties" (CRITICAL, 85.0) -> regex: `(actual knowledge of the chief executive|without any duty of reasonable inquiry|does not warrant.*infringe|freedom to operate)`
     4. "IP Ownership & Commercialization" (HIGH, 82.0) -> regex: `(jointly by developer and sponsor|without obtaining the consent of, or accounting|grant-back|irrevocably assigns|foreground ip)`
     5. "Escrow & Operational Covenants" (HIGH, 78.0) -> regex: `(earn-out|unfettered operational discretion|escrow release|technology escrow|working capital statement)`
     6. "Limitation of Liability & Super-Caps" (HIGH, 75.0) -> regex: `(limitation of liability|aggregate liability|consequential damages|super-cap)`
     7. "Service Level & Remedies" (HIGH, 72.0) -> regex: `(monthly uptime|service level|service credit|exclusive financial remedy|rto|rpo)`
     8. "Restrictive Covenants & Non-Compete" (MEDIUM, 65.0) -> regex: `(non-competition|five \(5\) consecutive years|directly or indirectly, anywhere in|non-solicitation)`
     9. "Termination & Remedies" (MEDIUM, 55.0) -> regex: `(termination|cure period|default|immediate termination)`
     10. "Governing Law & Dispute Venue" (MEDIUM, 50.0) -> regex: `(substantive laws of switzerland|icc rules of arbitration|geneva, switzerland|courts of london|governing law)`
   - Prompts the LLM (or falls back) to generate an opening Auditor Statement.
   - Logs execution latency and token metrics via `token_tracker`.

2. `opposing_node`:
   - Reviews the top 4 flagged risks.
   - Prompts the LLM: "You are aggressive Opposing Counsel... defend your client's position, push back against the auditor's claim, and propose a realistic, commercially viable compromise."
   - Includes deterministic sophisticated legal fallback arguments per category if LLM is offline.
   - Appends arguments to the `debate_transcript`.

3. `redline_node`:
   - Synthesizes balanced consensus text for each flagged risk.
   - Invokes `diff_engine.generate_clause_diff()` to generate word-level diff tokens.
   - Calculates composite score: `overall_score = round(min(100.0, total_score / max(1, num_risks)), 1)`.
   - Generates Redline Synthesizer consensus statement for the transcript.

4. `obligation_node`:
   - Extracts structured contractual obligations across 10 distinct patterns:
     1. Security Incident Notice (within 24h of trigger, critical)
     2. Escrow Deposit & Maintenance (quarterly, critical)
     3. SLA Credit Remittance (monthly, critical)
     4. Working Capital True-Up (90-day trigger, critical)
     5. Royalty & Milestone Remittance (quarterly, critical)
     6. Payment (Net 30, critical)
     7. Data Destruction & Sanitization (one-time post termination, critical)
     8. Audit & Compliance (annual SOC 2 / ISO inspection)
     9. Insurance (maintain $2M - $5M coverage, critical)
     10. Confidentiality (survives 5 years, critical)
   - Outputs structured records: `{id, clause_reference, obligor, recipient, obligation_type, description, due_date_or_trigger, recurrence, penalty_for_breach, is_critical}`.

After completing the nodes, commits the final results to the SQLite `contracts` database.

================================================================================
7. MULTI-PROVIDER LLM GATEWAY & FALLBACK SIMULATOR
================================================================================
`app/agents/llm_client.py`:
Implement async `call_llm(prompt, system_prompt, provider, model_name, use_local, temperature)`:
- Provider Priority:
  1. If `use_local` or `provider == 'ollama'`: POST to `http://localhost:11434/api/generate` with model `qwen3.5:4b`.
  2. If `provider == 'gemini'` or `GEMINI_API_KEY`: Call Google Generative Language API v1beta `gemini-3.5-flash-lite:generateContent`.
  3. If `provider == 'openai'` or `OPENAI_API_KEY`: Call OpenAI `v1/chat/completions`.
  4. If `provider == 'anthropic'` or `ANTHROPIC_API_KEY`: Call Anthropic `v1/messages`.
  5. Fallback: If network fails or keys are absent, return deterministic high-caliber legal responses with latency calculation so the app never crashes.

================================================================================
8. WORD (.DOCX) OPENXML TRACK CHANGES ENGINE (WITH DECISION BRANCHING)
================================================================================
`app/services/diff_engine.py`:
- Use `difflib.SequenceMatcher` over word arrays.
- Output array of diff tokens: `{"type": "equal"|"delete"|"insert", "text": "..."}`.

`app/services/export_service.py`:
- Creates native Word document using `python-docx`.
- Uses low-level OpenXML (`from docx.oxml import OxmlElement, qn`):
  - For deletions:
    Create `<w:del w:id="{id}" w:author="ContractMind Legal AI" w:date="{utc_iso}">`.
    Inside, create `<w:r>`, `<w:rPr><w:strike/><w:color w:val="DC2626"/></w:rPr>`, and `<w:delText>{text}</w:delText>`.
    Append to `paragraph._p`.
  - For insertions:
    Create `<w:ins w:id="{id}" w:author="ContractMind Legal AI" w:date="{utc_iso}">`.
    Inside, create `<w:r>`, `<w:rPr><w:u w:val="single"/><w:color w:val="16A34A"/></w:rPr>`, and `<w:t>{text}</w:t>`.
    Append to `paragraph._p`.
- Formats overview table displaying: Section, Severity, Redline Type, Decision Status ("Accepted", "Rejected", or "Pending Review").
- For Detailed Clauses:
  - Heading incorporates decision: `Section {sec_num} [Severity: {severity} | Decision: {status_text}]`.
  - If `accepted is False` (Rejected):
    Displays bold `Decision: REJECTED (Original Clause Retained):` and outputs the clean original text without insertions.
  - If `accepted is True` or `None` (Accepted or Pending Review):
    Displays bold `Decision: {STATUS} (Track Changes XML Enabled):` and injects native `<w:ins>` and `<w:del>` tokens.
- Saves file to `settings.EXPORT_DIR` and returns the file path.

================================================================================
9. MODEL CONTEXT PROTOCOL (MCP) SERVER
================================================================================
`app/mcp_server/server.py`:
- Implement `FastContractMCPServer`:
  - `list_tools()`:
    1. `evaluate_clause`: inputs `clause_text` (str), `clause_type` (str).
    2. `get_playbook_rules`: inputs `playbook_id` (optional str).
    3. `calculate_risk_matrix`: inputs `flagged_counts` ({critical, high, medium}).
  - `call_tool(tool_name, arguments)`:
    - `evaluate_clause`: matches domain-specific risk signals (e.g. "unlimited", "tipping basket", "without accounting", "immediate termination"). Returns `{clause_type, is_compliant, risk_level, flagged_signals, standard_policy, recommended_action}`.
    - `calculate_risk_matrix`: computes `score = min(100.0, 35*critical + 20*high + 10*medium)` and gives verdict `"REJECT / REDLINE"` or `"APPROVED WITH CAUTION"`.
- Expose via FastAPI:
  - `GET /mcp/tools` -> `{"tools": mcp_server.list_tools()}`
  - `POST /mcp/call` -> `{"result": mcp_server.call_tool(name, args)}`

================================================================================
10. TOKEN & COST TELEMETRY ENGINE
================================================================================
`app/core/token_tracker.py`:
- Token Estimation: `max(1, len(text) // 4)`.
- Pricing Table (USD per 1,000 tokens):
  - `gemini-3.5-flash-lite`: Prompt $0.000075, Completion $0.0003
  - `gpt-4o`: Prompt $0.005, Completion $0.015
  - `claude-3-5-sonnet`: Prompt $0.003, Completion $0.015
  - `deepseek-r1`: Prompt $0.00055, Completion $0.00219
  - `ollama`: $0.00 / $0.00
  - `default`: Prompt $0.002, Completion $0.008
- Method `log_execution(db, contract_id, agent_name, action, prompt_text, completion_text, latency_ms, model_name)`:
  Computes cost, commits `AuditLog` row to SQLite database, and returns the record.

================================================================================
11. INTERACTIVE REDLINE DECISIONS, AI PROMPT REWRITING & RISK-LEVEL FILTERING ENGINE
================================================================================
Implement full lawyer-in-the-loop revision controls with risk-level browsing and on-demand synthesis:

1. Risk-Level & Decision Status Browsing / Filtering:
   - Purpose: Lawyers reviewing high-stakes enterprise contracts need to triage redlines efficiently—focusing immediately on Critical and High risks before reviewing moderate and minor changes.
   - Filtering Controls:
     - Risk Severity Filter: `ALL` (default), `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
     - Decision Status Filter: `ALL` (default), `PENDING`, `ACCEPTED`, `REJECTED`.
   - UI Architecture:
     - Dynamic Filter Bar located directly above the redline diff stream.
     - Interactive pills displaying live badge counts computed reactively:
       - `All (count)`: Total redlines.
       - `Critical (count)`: Red badge with pulsating alert.
       - `High (count)`: Amber badge.
       - `Medium (count)`: Blue badge.
       - `Low (count)`: Slate/neutral badge.
     - Decision pills displaying live status counts:
       - `All (count)`
       - `Pending (count)`: Slate clock icon.
       - `Accepted (count)`: Green checkmark icon.
       - `Rejected (count)`: Red cross icon.
     - Live Counter & Active State Indicator:
       "Showing X of Y redlines • Filtered by [SEVERITY] risk • Status: [DECISION]".
     - Quick "Reset filters" action button.
     - Friendly Empty State: If no redlines match the selected criteria, display an intuitive empty-state card with a "Show All Redlines" button to restore full view.
   - REST API Filter Support:
     - Endpoint: `GET /api/v1/analysis/{contract_id}/redlines`
     - Query Parameters:
       - `risk_severity`: Optional string (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `ALL`). Case-insensitive.
       - `decision`: Optional string (`accepted`, `rejected`, `pending`, `ALL`). Case-insensitive.
     - Logic: Returns only the matching subset of redline dictionaries.

2. Accepting / Rejecting Changes:
   - Endpoint: `PATCH /api/v1/analysis/{contract_id}/redlines/{redline_id}`
   - Body: `{"accepted": true | false | null}`
   - Updates `contract.redlines` record in the database.
   - Reflected dynamically in the UI and in the Word DOCX export.

3. Rewriting Prompts & Regenerating Clauses:
   - Endpoint: `POST /api/v1/analysis/{contract_id}/redlines/{redline_id}/regenerate`
   - Body: `{"custom_prompt": str, "provider": Optional[str], "model_name": Optional[str]}`
   - Logic:
     1. Locates target redline from `contract.redlines`.
     2. Constructs LLM prompt:
        ```
        You are an expert corporate legal counsel and contract redline synthesizer.
        Original Contract Clause (Section {sec_num}):
        """{orig_text}"""

        Prior Proposed Redline:
        """{curr_sugg}"""

        USER CUSTOM REWRITE INSTRUCTION:
        """{req.custom_prompt}"""

        Task: Rewrite the contract clause replacement strictly following the user's custom instruction.
        Return ONLY valid JSON in this exact structure without markdown fences:
        {
          "suggested_text": "<exact revised clause replacement text>",
          "legal_rationale": "<concise explanation of how this satisfies the user prompt>"
        }
        ```
     3. Calls `llm_client.call_llm` with temperature 0.2.
     4. Recomputes word-level diff tokens using `diff_engine.generate_clause_diff`.
     5. Resets decision `accepted = None` and attaches `custom_prompt`.
     6. Appends a new turn to `contract.debate_transcript` tagged as `agent_name: "Client Prompt & Arbiter"`.
     7. Commits to DB and returns the updated redline object to the client.

================================================================================
12. FASTAPI REST API & STREAMING ENDPOINTS
================================================================================
Expose the following endpoints in `backend/app/main.py` and `api/v1/`:
- `POST /api/v1/contracts/upload`: Multi-part PDF upload, extracts sections, indexes into ChromaDB, creates contract row.
- `POST /api/v1/contracts/demo/{sample_type}`: Instant load & auto-analysis of benchmark contracts (`ma`, `cloud_dpa`, `joint_ip`, `msa`, `saas`, `nda`). Accepts `llm_provider`, `model_name`, and `playbook` query params.
- `GET /api/v1/contracts/`: List all analyzed contracts ordered by `created_at DESC`.
- `GET /api/v1/contracts/{id}`: Detailed view of contract, risks, transcript, redlines, and obligations.
- `DELETE /api/v1/contracts/{id}`: Deletes contract row, associated audit logs, and deletes ChromaDB collection.
- `POST /api/v1/analysis/{id}/trigger`: Triggers orchestrator execution.
- `GET /api/v1/analysis/{id}/redlines`: Retrieves list of structured redlines with optional `risk_severity` and `decision` filters.
- `PATCH /api/v1/analysis/{id}/redlines/{redline_id}`: Accepts or rejects a specific redline.
- `POST /api/v1/analysis/{id}/redlines/{redline_id}/regenerate`: Rewrites and re-synthesizes redline from custom prompt.
- `GET /api/v1/analysis/{id}/export/docx`: Downloads `.docx` with native Word Track Changes respecting accepted/rejected choices.
- `GET /api/v1/analysis/audit/summary`: Computes total tokens, total cost USD, average latency ms, and execution breakdown.
- `DELETE /api/v1/analysis/audit/reset`: Clears all audit log telemetry records.
- `GET /api/v1/analysis/llm/config`: Checks status of Gemini key, Ollama endpoint, OpenAI key, and Anthropic key.
- `POST /api/v1/analysis/llm/config`: Allows runtime update of API keys.
- `GET /health`: Health check JSON (`{"status": "healthy", "version": "1.5.0"}`).
- `GET /` & `GET /studio`: Serves `backend/static/index.html`.

================================================================================
13. FRONTEND: ALPINE.JS & TAILWIND NEO-LEGAL STUDIO
================================================================================
Implement `backend/static/index.html`:
- Typography: Plus Jakarta Sans (body, headers), JetBrains Mono (badges, metrics, diff tokens).
- Color Palette:
  - Background: `#F4F6FC` with subtle multi-color radial blur gradients.
  - Brand accents: `#5B67F6`, `#6366F1`.
  - Pastel card tags: Pink (`#FFF0F3`), Blue (`#EEF6FF`), Amber (`#FFF6EE`), Purple (`#F7EEFD`), Emerald (`#F0FAF2`).
  - Dark elements: Slate-900 `#1E2238`.
- Interactive Features:
  1. Top Navigation Bar:
     - Hamburger toggle opening slide-out system drawer.
     - Brand logo with gradient scale icon and `v1.5` badge.
     - View switcher pills: "Ingestion Studio" vs "Telemetry & Audits".
     - Live Engine status pill with pulsating ping dot (Green = Online, Amber = Standby) and model label.
     - Settings avatar modal trigger.
  2. Starting Instructions Banner:
     - Prominent dismissible card for first-time users explaining the 3-step workflow: Upload -> Multi-Agent Debate -> Track Changes Word Export.
  3. Interactive Guided Rundown Tour:
     - Triggered by floating or header Question Mark button (`?`).
     - Includes initial pulsating notification bubble: `"Click here for a rundown"`.
     - When active:
       - Screen dims with backdrop blur (`fixed inset-0 bg-slate-950/50`).
       - Targeted element receives `.tour-spotlight-active` with intense pulsing halo:
         `box-shadow: 0 0 0 11px rgba(91, 103, 246, 0.8), 0 0 70px rgba(91, 103, 246, 0.8)`.
       - Floating tour dialog advances through 7 steps with Next, Back, and Skip controls.
  4. Benchmark Contracts Hub:
     - 6 one-click cards with preset risk badges:
       - Cross-Border M&A (Risk: 87, Tipping baskets & IP trap)
       - Cloud AI & DPA (Risk: 79, Model training on data & SLAs)
       - AI Joint R&D (Risk: 83, Joint IP without accounting)
       - Enterprise MSA (Risk: 65, Uncapped indemnity & caps)
       - SaaS Agreement (Risk: 50, Auto-renewal lock-in)
       - Mutual NDA (Risk: 25, Standard confidentiality)
  5. Interactive Redlines Hub (with Risk Filtering, Accept, Reject, Reset & AI Rewriter):
     - Redlines Risk & Decision Filter Toolbar:
       - Risk Severity Filter Pills: `All`, `Critical` (red badge), `High` (amber badge), `Medium` (blue badge), and `Low` (slate badge) with reactive count indicators (`countRedlinesByRisk(sev)`).
       - Decision Status Filter Pills: `All`, `Pending` (slate), `Accepted` (green), and `Rejected` (red) with reactive count indicators (`countRedlinesByDecision(dec)`).
       - Filter Status Summary: Live indicator showing `"Showing X of Y redlines • Filtered by [Severity] risk • Status: [Decision]"`.
       - Quick "Reset filters" link button.
       - Empty State Card: When 0 clauses match the active filter, displays a clear notification with a "Show All Redlines" reset button.
     - Displays per-clause card with risk severity and legal rationale.
     - Word-level insertions rendered as `<span class="diff-ins">` (emerald background, green text, underline).
     - Word-level deletions rendered as `<span class="diff-del">` (red background, red text, strike-through).
     - Decision Badges:
       - Green badge: `<i class="fa-solid fa-circle-check"></i> Accepted`
       - Red badge: `<i class="fa-solid fa-circle-xmark"></i> Rejected`
       - Slate badge: `<i class="fa-regular fa-clock"></i> Pending Review`
     - Action Toolbar:
       - **Accept** button: toggles `accepted = true`, calls `PATCH` endpoint, turns solid green.
       - **Reject** button: toggles `accepted = false`, calls `PATCH` endpoint, turns solid red.
       - **Reset** button: clears choice back to pending review.
       - **Rewrite with AI Prompt** button: expands inline AI prompt rewriter panel.
     - Inline AI Prompt Rewriter Panel:
       - Custom input box: `x-model="rewritePrompts[rl.id]"` with placeholder `"e.g. Make mutual, cap liability at $1M, add 15-day cure window..."`.
       - Quick instruction chips:
         - `+ Make Mutual`
         - `+ 1x Annual Cap`
         - `+ 30-Day Cure`
         - `+ Strike AI Training`
       - **Regenerate Redline** button: executes `POST .../regenerate`, triggers spinner, re-synthesizes clause and diff tokens live.
     - "Export Word Track Changes (.docx)" button triggering direct file download reflecting decisions.
  6. Obligations Matrix:
     - Tabular layout with columns: Citation, Category, Obligor, Recipient, Trigger/Due Date, Recurrence, and Penalty.
     - Critical items marked with red alert badges.
  7. Telemetry & Audits Dashboard:
     - KPI cards: Total Tokens Processed, Total Cloud Cost USD, Average Node Latency, Active LLM Core.
     - Execution log table with agent name, prompt/completion tokens, latency, cost, and timestamps.
     - "Reset Metrics" button with confirmation modal.
  8. Settings & API Keys Modal:
     - Inputs for Gemini API Key, OpenAI API Key, Anthropic API Key, and Ollama Base URL.
     - Radio selector for LLM Provider (Google Gemini, Local Ollama, OpenAI GPT-4o, Anthropic Claude).
     - Radio selector for Negotiation Playbook (Strict Enterprise, Balanced Commercial, Founder Friendly).

================================================================================
14. DEPLOYMENT & PRODUCTION ORCHESTRATION
================================================================================
1. Local 1-Click Launch:
   - `run_contractmind.bat`: Checks for Python, installs requirements, executes `python launch.py`.
   - `launch.py`: Creates required directories, runs DB migration, launches Uvicorn on `0.0.0.0:8000`, redirects logs to `backend/backend.log`, and opens default web browser to `http://localhost:8000`.

2. Vercel Multi-Service Deployment (`vercel.json`):
   ```json
   {
     "$schema": "https://openapi.vercel.sh/vercel.json",
     "services": {
       "backend": {
         "root": "backend",
         "framework": "fastapi"
       },
       "frontend": {
         "root": "frontend",
         "framework": "nextjs",
         "bindings": [
           {
             "type": "service",
             "service": "backend",
             "format": "url",
             "env": "BACKEND_URL"
           }
         ]
       }
     },
     "rewrites": [
       { "source": "/api/(.*)", "destination": { "service": "backend" } },
       { "source": "/health", "destination": { "service": "backend" } },
       { "source": "/docs", "destination": { "service": "backend" } },
       { "source": "/openapi.json", "destination": { "service": "backend" } },
       { "source": "/mcp/(.*)", "destination": { "service": "backend" } },
       { "source": "/studio", "destination": { "service": "backend" } },
       { "source": "/static/(.*)", "destination": { "service": "backend" } },
       { "source": "/(.*)", "destination": { "service": "frontend" } }
     ]
   }
   ```
3. Frontend Next.js Bridge (`frontend/app/route.ts`):
   - Implements dynamic GET route handler that reads `frontend/public/index.html` (the identical Alpine.js v1.5 UI) and returns it with `Content-Type: text/html`.
   - `frontend/next.config.js` redirects `/audit` and `/contracts/*` to `/`, and rewrites `/api/v1/*` to `BACKEND_URL`.
   - Guarantees that whether deployed on Vercel as a multi-service project, as a standalone Next.js project, or run locally, users always receive the latest ContractMind v1.5 Studio.

================================================================================
15. VERIFICATION CHECKLIST
================================================================================
Ensure the completed codebase satisfies all criteria:
1. [x] Zero hardcoded API keys in tracked files (use .env.example).
2. [x] PyMuPDF table parser generates valid Markdown tables.
3. [x] PII redactor removes SSNs, credit cards, bank accounts before embedding.
4. [x] ChromaDB indices are purged on contract deletion.
5. [x] Clause-level Accept / Reject decisions persist via PATCH endpoint and update UI state.
6. [x] Clause-level AI Prompt Rewriting endpoint generates custom redlines with live diff tokens.
7. [x] DOCX export reflects Accept / Reject decisions in summary table and detailed clause headings.
8. [x] Real measured time.time() latency logged for all agent nodes.
9. [x] Token pricing correctly applies to Gemini, OpenAI, Claude, and Ollama.
10. [x] MCP server conforms to JSON-RPC tools schema at /mcp/tools and /mcp/call.
11. [x] Frontend features 7-step guided tour with glowing halo spotlight and notification bubble.
12. [x] `npm run build` on frontend completes with zero TypeScript or lint errors.
13. [x] Redline risk-level filtering (Critical, High, Medium, Low) and decision status filtering (Pending, Accepted, Rejected) with reactive count badges and empty-state recovery.
14. [x] Backend endpoint `GET /api/v1/analysis/{contract_id}/redlines` supports `risk_severity` and `decision` query parameter filtering.
```
