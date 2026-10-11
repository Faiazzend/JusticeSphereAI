# 🏛️ ContractMind v1.5.3 — The Ultimate Master Architecture & Reproduction Prompt (A-Z)

> **Document Version:** 1.5.3  
> **Target Project:** ContractMind v1.5.3 (Autonomous Multi-Agent Legal AI Studio)  
> **Track:** JusticeSphere_AI — AI Builders Congress 2026  
> **Repository:** [https://github.com/Faiazzend/JusticeSphereAI](https://github.com/Faiazzend/JusticeSphereAI)

---

```markdown
You are an elite Principal AI Systems Architect, Security Engineer, and Legal Tech Specialist.
Build "ContractMind v1.5.3" completely from scratch: an enterprise-grade, autonomous multi-agent legal intelligence platform that ingests complex commercial contracts, conducts adversarial negotiation debate, synthesizes consensus redlines with authentic Word OpenXML Track Changes, extracts structured obligation matrices, enables live Server-Sent Events (SSE) streaming, provides multi-format compliance exports (Word, RFC 5545 iCalendar .ics, JSON, CSV), compares contracts with risk deltas, manages custom negotiation playbooks, offers multi-provider LLM latency health probes, and features an interactive Alpine.js Neo-Legal Studio with risk-level browsing, lawyer-in-the-loop clause decisions, and AI prompt rewriting.

Implement the system strictly following the exact architectural specifications, database schemas, agent graphs, styling design system, and API protocols specified below. Zero shortcuts, zero elisions, zero placeholders.

================================================================================
TABLE OF CONTENTS
================================================================================
1. High-Level Architecture & Technical Stack
2. Directory Structure & File Hierarchy
3. Database Models & Schema Specifications (Contract, AuditLog, User)
4. PDF Ingestion, Table Extraction & PII Redaction Engine
5. Contextual RAG & Semantic Chunking Engine (ChromaDB + Fallback)
6. Multi-Agent StateGraph Pipeline (4 Agents with Per-Node Isolation & Resilient Event Broadcasting)
7. Multi-Provider LLM Gateway, Health Probes & Fallback Simulator
8. Word (.docx) OpenXML Track Changes Engine (Decision Branching & Non-Blocking I/O)
9. Multi-Format Legal Export Suite (Word DOCX, RFC 5545 iCalendar, JSON, CSV)
10. Contract Comparison & Risk Delta Engine
11. Custom Playbook Management System (CRUD API)
12. User Authentication & Security Layer
13. Model Context Protocol (MCP) Server
14. Token & Cost Telemetry Engine
15. Interactive Redline Decisions, AI Prompt Rewriting & Risk-Level Filtering
16. FastAPI REST API & SSE Streaming Specification
17. Frontend: Alpine.js 3.14 & Tailwind CSS Neo-Legal Studio
18. Deployment & Production Orchestration (Local & Vercel Multi-Service)
19. Verification & Automated Test Suite (16/16 Pytest Specifications)

================================================================================
1. HIGH-LEVEL ARCHITECTURE & TECHNICAL STACK
================================================================================
- Backend Framework: FastAPI (Python 3.10+) with async endpoints, lifespan DB initialization, and CORS middleware configured for full client origin access.
- Database: SQLite with async SQLAlchemy 2.0 (aiosqlite). Fallback to /tmp paths if VERCEL=1 or read-only filesystem environment is detected.
- Vector Engine: ChromaDB persistent client with automatic fallback to in-memory term-frequency cosine scorer.
- Document Processing: PyMuPDF (fitz) for text extraction, native PDF table detection converted to Markdown tables, and regex-based PII redaction.
- Agent Architecture: StateGraph pattern with 4 specialized roles:
  1. Auditor Agent (Policy defender, scans 10 risk categories with regex, LLM statement generation, token & latency logging).
  2. Opposing Counsel Agent (Counterparty negotiator, aggressive commercial defense, compromise proposal).
  3. Redline Synthesizer Agent (Consensus arbiter, word-level SequenceMatcher diff tokens, composite risk scoring).
  4. Obligation Extractor Agent (Calendar extractor, role matrix, penalty monitor, extracts 10 obligation patterns).
- Resilience & Event Broadcasting:
  - Per-node failure isolation: each graph node wrapped in try/except; on exception, node logs error, records fallback turn, and allows subsequent nodes to proceed.
  - EventBroadcaster: in-memory pub/sub publishing agent lifecycle events to async queues for real-time SSE streaming.
- Real-Time Live Streaming:
  - Server-Sent Events (SSE) endpoint at `/api/v1/stream/debate/{contract_id}` with standard headers (`Cache-Control: no-cache`, `X-Accel-Buffering: no`), replaying history for completed contracts, streaming live node events, and periodic `: ping\n\n` comments.
- Word Track Changes (.docx):
  - python-docx with custom OpenXML manipulation injecting low-level `<w:ins>` and `<w:del>` elements with author attribution and UTC timestamps.
  - Decision branching: Accepted/Pending redlines include tracked changes; Rejected redlines retain original clause cleanly.
  - Non-blocking execution via `asyncio.to_thread`.
- Multi-Format Export Suite:
  - Word (.docx) with authentic Track Changes.
  - iCalendar (.ics) RFC 5545 compliance calendar with VEVENT entries for deadlines.
  - Audit JSON (.json) complete contract intelligence dump.
  - Tabular CSV (.csv) RFC 4180 obligations and redlines matrix.
- Contract Comparison:
  - Side-by-side section comparison diffing text tokens and calculating overall risk score delta.
- Custom Playbooks:
  - CRUD API managing custom institutional negotiation policies alongside built-in standard playbooks.
- LLM Gateway & Health Telemetry:
  - Google Gemini default core (gemini-2.0-flash / gemini-1.5-flash / gemini-3.5-flash-lite), Ollama local core (qwen3.5:4b), OpenAI (gpt-4o), Anthropic (claude-3-5-sonnet).
  - 60-second timeouts, 4096 maxOutputTokens.
  - Real-time provider health diagnostic endpoint (`/api/v1/analysis/llm/health`).
  - High-fidelity deterministic legal fallback simulator if network or API keys are unavailable.
- User Authentication:
  - Salted SHA-256 password hashing, HMAC bearer tokens, register/login/me endpoints.
- Protocol: Model Context Protocol (MCP) JSON-RPC tools gateway at `/mcp/tools` and `/mcp/call`.
- Frontend: Single-Page Application (SPA) built using Alpine.js 3.14, Tailwind CSS, FontAwesome 6, Plus Jakarta Sans, and JetBrains Mono. Dual-served via FastAPI (`backend/static/index.html`) and Next.js 14 bridge (`frontend/public/index.html` + `frontend/app/route.ts`).
  - Features a 7-step guided rundown tour with high-intensity glowing halo spotlights (`#5B67F6`).
  - Redline risk-level filtering (Critical, High, Medium, Low) and decision status filtering (Pending, Accepted, Rejected) with reactive count badges.
  - Inline Accept / Reject / Reset buttons and inline AI prompt rewriter with quick chips.
  - Side-by-side contract comparison modal and LLM health diagnostic modal.

================================================================================
2. DIRECTORY STRUCTURE & FILE HIERARCHY
================================================================================
```
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── nodes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auditor_agent.py
│   │   │   │   ├── obligation_agent.py
│   │   │   │   ├── opposing_agent.py
│   │   │   │   └── redline_agent.py
│   │   │   ├── __init__.py
│   │   │   ├── graph.py
│   │   │   ├── llm_client.py
│   │   │   └── state.py
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── analysis.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── contracts.py
│   │   │   │   ├── playbook.py
│   │   │   │   └── stream.py
│   │   │   ├── __init__.py
│   │   │   └── deps.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── pii_redactor.py
│   │   │   ├── security.py
│   │   │   └── token_tracker.py
│   │   ├── mcp_server/
│   │   │   ├── __init__.py
│   │   │   └── server.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── audit.py
│   │   │   ├── contract.py
│   │   │   └── user.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── contract_schemas.py
│   │   │   ├── obligation_schemas.py
│   │   │   ├── playbook_schemas.py
│   │   │   └── risk_schemas.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── diff_engine.py
│   │   │   ├── export_service.py
│   │   │   ├── pdf_processor.py
│   │   │   └── rag_engine.py
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── static/
│   │   └── index.html
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_api_integration.py
│   │   ├── test_contractmind.py
│   │   ├── test_v152_features.py
│   │   └── test_v153_enhancements.py
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
│   ├── ai_joint_rd.txt
│   ├── cloud_ai_dpa.txt
│   ├── cross_border_ma.txt
│   ├── enterprise_msa.txt
│   ├── mutual_nda.txt
│   └── saas_agreement.txt
├── .env.example
├── .gitignore
├── launch.py
├── pytest.ini
├── run_contractmind.bat
├── vercel.json
├── MASTER_PROMPT.md
└── README.md
```

================================================================================
3. DATABASE MODELS & SCHEMA SPECIFICATIONS
================================================================================
Implement async SQLAlchemy 2.0 models with declarative base:

1. `Contract` (`backend/app/models/contract.py`):
   - `id`: String(36), primary key (UUID string).
   - `title`: String(255), nullable=False.
   - `original_filename`: String(255), nullable=False.
   - `file_path`: String(512), nullable=False.
   - `status`: String(50), default="uploaded" ("uploaded", "processing", "analyzed", "error").
   - `overall_risk_score`: Float, default=0.0 (0.0 to 100.0 scale).
   - `raw_text`: Text, nullable=False.
   - `playbook_name`: String(100), default="Standard Corporate Playbook".
   - `extracted_sections`: JSON, default=list (items: `{section_number, title, content, page_number}`).
   - `identified_risks`: JSON, default=list (items: `{category, risk_level, score, rationale, mitigation, section_reference}`).
   - `debate_transcript`: JSON, default=list (items: `{agent_name, timestamp, content, target_clause}`).
   - `redlines`: JSON, default=list (items: `{id, section_number, original_text, suggested_text, diff_type, risk_severity, legal_rationale, diff_tokens, accepted, custom_prompt}`).
   - `obligations`: JSON, default=list (items: `{id, clause_reference, obligor, recipient, obligation_type, description, due_date_or_trigger, recurrence, penalty_for_breach, is_critical}`).
   - `risk_summary`: JSON, default=dict (keys: `critical`, `high`, `medium`, `low`, total integer counts).
   - `created_at`: DateTime(timezone=True), default=datetime.utcnow.
   - `updated_at`: DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow.

2. `AuditLog` (`backend/app/models/audit.py`):
   - `id`: Integer, primary key, autoincrement=True.
   - `contract_id`: String(36), ForeignKey("contracts.id", ondelete="CASCADE"), nullable=True.
   - `agent_name`: String(100), nullable=False.
   - `action`: String(100), nullable=False.
   - `prompt_tokens`: Integer, default=0.
   - `completion_tokens`: Integer, default=0.
   - `total_tokens`: Integer, default=0.
   - `latency_ms`: Float, default=0.0.
   - `model_name`: String(100), default="gemini-2.0-flash".
   - `estimated_cost_usd`: Float, default=0.0 (precision 6 decimal places).
   - `details`: Text, nullable=True.
   - `created_at`: DateTime(timezone=True), default=datetime.utcnow.

3. `User` (`backend/app/models/user.py`):
   - `id`: String(36), primary key (UUID string).
   - `username`: String(100), unique=True, index=True, nullable=False.
   - `hashed_password`: String(255), nullable=False.
   - `email`: String(255), unique=True, index=True, nullable=True.
   - `role`: String(50), default="lawyer".
   - `created_at`: DateTime(timezone=True), default=datetime.utcnow.

================================================================================
4. PDF INGESTION, TABLE EXTRACTION & PII REDACTION ENGINE
================================================================================
1. `backend/app/core/pii_redactor.py`:
   - Compiled regex signatures:
     - SSN: `r"\b\d{3}-\d{2}-\d{4}\b"`
     - Credit Card: `r"\b(?:\d{4}[-\s]?){3}\d{4}\b"`
     - Email: `r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"`
     - Phone: `r"\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b"`
     - Bank Account: `r"\b\d{8,17}\b"`
     - Tax ID: `r"\b\d{2}-\d{7}\b"`
   - `redact(text: str) -> Tuple[str, Dict[str, int]]`:
     Iterates patterns, replaces matches with `[REDACTED_{TYPE}]`, tracks replacement count per category.

2. `backend/app/services/pdf_processor.py`:
   - Uses PyMuPDF (`import fitz`).
   - `process_pdf(file_path: str) -> Tuple[str, List[Dict[str, Any]]]`:
     - Reads pages, extracts raw text via `page.get_text("text")`.
     - Detects tabular exhibits via `page.find_tables()`. Converts table matrices into clean Markdown tables:
       `| Header 1 | Header 2 |\n| --- | --- |\n| Cell 1 | Cell 2 |`
     - Concatenates full text and applies `pii_redactor.redact()`.
     - Splits text into structured sections using section header regex:
       `r"(?:\n|^)(?:SECTION|ARTICLE|CLAUSE)?\s*(\d+(?:\.\d+)*|[IVXLCDM]+)[\.\:\-\s]+([A-Z][A-Za-z0-9\s\,\-\&\/\(\)]+)(?=\n)"`
     - If fewer than 2 headers matched, falls back to paragraph/block chunking.
     - Returns clean concatenated text and list of section objects `{section_number, title, content, page_number}`.

================================================================================
5. CONTEXTUAL RAG & SEMANTIC CHUNKING ENGINE
================================================================================
`backend/app/services/rag_engine.py`:
- Contextual Semantic Chunking:
  - For each section, chunks longer than 1500 characters are split along paragraph boundaries.
  - Every chunk receives a prepended contextual metadata header:
    ```
    [Document: {contract_title} | Section: {sec_num} ({title}) | Page: {page}]
    Context: This excerpt defines terms and legal obligations governing {title.lower()}.
    ```
- ChromaDB Vector Storage & In-Memory Fallback:
  - Initializes `chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)`.
  - Creates/retrieves collection: `f"contract_{contract_id.replace('-', '_')}"`.
  - Upserts chunk documents, IDs, and metadata.
  - Maintains `self._memory_store[contract_id] = chunks` for instantaneous fallback.
  - On `query(contract_id, query_text, n_results=4)`:
    - Queries ChromaDB collection.
    - If ChromaDB raises an exception or returns empty, executes in-memory term-frequency cosine scoring over `self._memory_store[contract_id]`.
  - `delete_contract(contract_id)`:
    - Purges collection from ChromaDB and frees memory from `self._memory_store`.

================================================================================
6. MULTI-AGENT STATEGRAPH PIPELINE (4 AGENTS)
================================================================================
`backend/app/agents/state.py`:
- `ContractReviewState(TypedDict)`:
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

`backend/app/agents/graph.py` & Agent Nodes:
1. `EventBroadcaster`:
   - Singleton broadcaster maintaining a list of active `asyncio.Queue` subscribers.
   - `subscribe() -> asyncio.Queue`, `unsubscribe(queue)`, `publish(event: dict)`.
   - Broadcasts events: `node_start`, `node_complete`, `pipeline_complete`, `node_error`.

2. Sequential Pipeline with Per-Node Failure Isolation:
   Every node execution is wrapped in a dedicated `try ... except` block. If an individual node encounters an unexpected failure, it logs the exception, adds a fallback turn to `debate_transcript`, updates `state["current_status"]`, and gracefully transfers execution to the subsequent node.

3. Agent Nodes:
   - `auditor_node` (`backend/app/agents/nodes/auditor_agent.py`):
     - Scans sections against 10 risk categories with compiled regex signatures:
       1. AI Training & Data Privacy (CRITICAL, 95.0) -> `(ingest, de-identify|foundational ai models|prompts|model checkpoints|training, tuning|training data|sub-processor)`
       2. Indemnification & Baskets (CRITICAL, 88.0) -> `(indemnif\w+|hold harmless|tipping basket|de minimis threshold|basket)`
       3. Representations & Warranties (CRITICAL, 85.0) -> `(actual knowledge of the chief executive|without any duty of reasonable inquiry|does not warrant.*infringe|freedom to operate)`
       4. IP Ownership & Commercialization (HIGH, 82.0) -> `(jointly by developer and sponsor|without obtaining the consent of, or accounting|grant-back|irrevocably assigns|foreground ip)`
       5. Escrow & Operational Covenants (HIGH, 78.0) -> `(earn-out|unfettered operational discretion|escrow release|technology escrow|working capital statement)`
       6. Limitation of Liability & Super-Caps (HIGH, 75.0) -> `(limitation of liability|aggregate liability|consequential damages|super-cap)`
       7. Service Level & Remedies (HIGH, 72.0) -> `(monthly uptime|service level|service credit|exclusive financial remedy|rto|rpo)`
       8. Restrictive Covenants & Non-Compete (MEDIUM, 65.0) -> `(non-competition|five \(5\) consecutive years|directly or indirectly, anywhere in|non-solicitation)`
       9. Termination & Remedies (MEDIUM, 55.0) -> `(termination|cure period|default|immediate termination)`
       10. Governing Law & Dispute Venue (MEDIUM, 50.0) -> `(substantive laws of switzerland|icc rules of arbitration|geneva, switzerland|courts of london|governing law)`
     - Synthesizes opening Auditor Statement via LLM or deterministic fallback.
     - Logs token telemetry via `token_tracker.log_execution()`.

   - `opposing_node` (`backend/app/agents/nodes/opposing_agent.py`):
     - Takes top 4 flagged risks from Auditor.
     - Role: Aggressive Opposing Counsel defending counterparty positions and offering commercial compromises.
     - Prompts LLM or uses deterministic high-caliber commercial compromise responses per category.
     - Appends response to `state["debate_transcript"]`.

   - `redline_node` (`backend/app/agents/nodes/redline_agent.py`):
     - Role: Redline Synthesizer Arbiter.
     - Reconciles Auditor and Opposing Counsel positions into balanced compromise clauses.
     - Uses `diff_engine.generate_clause_diff(orig_text, suggested_text)` to generate word-level diff tokens (`equal`, `delete`, `insert`).
     - Calculates composite risk score: `overall_score = round(min(100.0, total_score / max(1, num_risks)), 1)`.
     - Appends Synthesizer statement to `debate_transcript`.

   - `obligation_node` (`backend/app/agents/nodes/obligation_agent.py`):
     - Extracts structured obligations across 10 distinct patterns:
       1. Security Incident Notice (within 24h, critical)
       2. Escrow Deposit & Maintenance (quarterly, critical)
       3. SLA Credit Remittance (monthly, critical)
       4. Working Capital True-Up (90-day trigger, critical)
       5. Royalty & Milestone Remittance (quarterly, critical)
       6. Payment Terms (Net 30, critical)
       7. Data Destruction & Sanitization (post-termination, critical)
       8. Audit & Compliance (annual SOC 2 / ISO inspection)
       9. Insurance Coverage (maintain $2M - $5M coverage, critical)
       10. Confidentiality Covenants (survives 5 years, critical)
     - Outputs list of obligation records: `{id, clause_reference, obligor, recipient, obligation_type, description, due_date_or_trigger, recurrence, penalty_for_breach, is_critical}`.

- Commits final state (`identified_risks`, `debate_transcript`, `redlines`, `obligations`, `risk_summary`, `overall_risk_score`, `status="analyzed"`) to SQLite `contracts` table.

================================================================================
7. MULTI-PROVIDER LLM GATEWAY, HEALTH PROBES & FALLBACK SIMULATOR
================================================================================
`backend/app/agents/llm_client.py`:
- Default Cloud Model: `gemini-2.0-flash` (with automatic fallback to `gemini-1.5-flash` or `gemini-3.5-flash-lite`).
- Timeout: 60.0 seconds with `maxOutputTokens: 4096`.
- Priority Hierarchy:
  1. If `use_local` or `provider == 'ollama'`: POST `http://localhost:11434/api/generate` (`qwen3.5:4b`).
  2. If `provider == 'gemini'` or `GEMINI_API_KEY`: Google Generative Language API v1beta endpoint.
  3. If `provider == 'openai'` or `OPENAI_API_KEY`: OpenAI chat completions `gpt-4o`.
  4. If `provider == 'anthropic'` or `ANTHROPIC_API_KEY`: Anthropic messages API `claude-3-5-sonnet`.
  5. Deterministic Legal Simulator: If keys are absent or calls fail, returns sophisticated domain-specific legal text with measured latency.
- Health Telemetry Endpoint (`GET /api/v1/analysis/llm/health`):
  - Sends a minimal latency probe prompt to each configured provider.
  - Measures round-trip ping time in milliseconds.
  - Returns `{providers: [{name, status, latency_ms, model, is_default, error}], active_provider, total_configured}`.

================================================================================
8. WORD (.DOCX) OPENXML TRACK CHANGES ENGINE (DECISION BRANCHING)
================================================================================
`backend/app/services/diff_engine.py`:
- `generate_clause_diff(original_text: str, suggested_text: str) -> List[Dict[str, str]]`:
  - Splits text into word tokens.
  - Uses `difflib.SequenceMatcher(None, orig_words, sugg_words).get_opcodes()`.
  - Produces list of tokens: `{"type": "equal"|"delete"|"insert", "text": "..."}`.

`backend/app/services/export_service.py`:
- OpenXML Track Changes Engine:
  - Instantiates `docx.Document()`.
  - Inserts low-level OpenXML tags using `docx.oxml.OxmlElement` and `docx.oxml.ns.qn`:
    - Deletion: `<w:del w:id="{id}" w:author="ContractMind Legal AI" w:date="{utc_now}">`
      containing `<w:r>`, `<w:rPr><w:strike/><w:color w:val="DC2626"/></w:rPr>`, and `<w:delText>{text}</w:delText>`.
    - Insertion: `<w:ins w:id="{id}" w:author="ContractMind Legal AI" w:date="{utc_now}">`
      containing `<w:r>`, `<w:rPr><w:u w:val="single"/><w:color w:val="16A34A"/></w:rPr>`, and `<w:t>{text}</w:t>`.
  - Overview Table:
    - Lists Section, Severity, Redline Type, Decision Status ("Accepted", "Rejected", or "Pending Review").
  - Detailed Clause Sections with Decision Branching:
    - Heading: `Section {sec_num} [Severity: {severity} | Decision: {status_text}]`.
    - If `accepted is False` (Rejected):
      Adds bold indicator `Decision: REJECTED (Original Clause Retained):` and outputs clean original clause text.
    - If `accepted is True` or `None` (Accepted or Pending Review):
      Adds bold indicator `Decision: {STATUS} (Track Changes XML Enabled):` and appends native `<w:ins>` and `<w:del>` XML runs to `paragraph._p`.
- Non-blocking execution: File creation and I/O wrapped in `asyncio.to_thread()` in `api/v1/analysis.py`.

================================================================================
9. MULTI-FORMAT LEGAL EXPORT SUITE (DOCX, ICALENDAR, JSON, CSV)
================================================================================
Expose 4 dedicated compliance export endpoints in `backend/app/api/v1/analysis.py`:

1. Word Track Changes (.docx):
   - Endpoint: `GET /api/v1/analysis/{contract_id}/export/docx`
   - Content-Type: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
   - Header: `Content-Disposition: attachment; filename="{title}_redlines.docx"`

2. iCalendar RFC 5545 Compliance Schedule (.ics):
   - Endpoint: `GET /api/v1/analysis/{contract_id}/export/calendar` (also `/export/ics`)
   - Content-Type: `text/calendar; charset=utf-8`
   - Header: `Content-Disposition: attachment; filename="{title}_obligations.ics"`
   - Generates RFC 5545 format with `BEGIN:VCALENDAR`, `VERSION:2.0`, `PRODID:-//ContractMind//Legal AI v1.5.3//EN`.
   - Each obligation emits a `BEGIN:VEVENT`:
     - `UID`: `{contract_id}_{obligation_id}@contractmind.ai`
     - `DTSTAMP`, `DTSTART`: Valid ISO-8601 UTC timestamp calculated from due date / trigger.
     - `SUMMARY`: `[{category}] {obligor} -> {recipient}`
     - `DESCRIPTION`: Full description with penalty for breach notes.
     - `PRIORITY`: `1` if critical, `5` otherwise.

3. Complete Audit JSON Dump (.json):
   - Endpoint: `GET /api/v1/analysis/{contract_id}/export/json`
   - Content-Type: `application/json`
   - Header: `Content-Disposition: attachment; filename="{title}_audit_dump.json"`
   - Returns full contract record, extracted sections, identified risks, debate transcript, redlines with decisions, obligations matrix, and risk summary.

4. Tabular CSV Matrix (.csv):
   - Endpoint: `GET /api/v1/analysis/{contract_id}/export/csv`
   - Query Parameter: `matrix_type` (`obligations` [default] or `redlines`).
   - Content-Type: `text/csv; charset=utf-8`
   - Header: `Content-Disposition: attachment; filename="{title}_{matrix_type}.csv"`
   - Formatted per RFC 4180 with standard CSV writer.

================================================================================
10. CONTRACT COMPARISON & RISK DELTA ENGINE
================================================================================
`backend/app/api/v1/contracts.py`:
- Endpoint: `POST /api/v1/contracts/compare`
- Request Body (`ContractCompareRequest`):
  - `source_contract_id`: str
  - `target_contract_id`: str
- Processing:
  - Fetches source and target contracts from DB.
  - Matches sections by section number or normalized title.
  - For matched sections, generates token-level diff using `diff_engine.generate_clause_diff()`.
  - Calculates risk score delta: `risk_delta = target.overall_risk_score - source.overall_risk_score`.
  - Classifies clauses into: `added_clauses`, `removed_clauses`, `modified_clauses`, `unmodified_clauses`.
- Response (`ContractCompareResponse`):
  - `{source_id, target_id, source_title, target_title, risk_delta, source_risk_score, target_risk_score, section_comparisons: [...], summary}`.

================================================================================
11. CUSTOM PLAYBOOK MANAGEMENT SYSTEM (CRUD API)
================================================================================
`backend/app/api/v1/playbook.py`:
- In-memory thread-safe dictionary store `CUSTOM_PLAYBOOKS: Dict[str, Dict]`.
- Endpoints:
  - `GET /api/v1/playbook/list`: Returns built-in standard playbooks (`Standard Corporate`, `Strict Enterprise`, `Founder Friendly`, `M&A Aggressive`).
  - `GET /api/v1/playbook/custom`: Lists all user-created custom playbooks.
  - `POST /api/v1/playbook/custom`: Creates a custom playbook.
    - Body: `{"name": str, "description": str, "rules": List[Dict], "risk_tolerance": float}`.
  - `DELETE /api/v1/playbook/custom/{name}`: Deletes a custom playbook.

================================================================================
12. USER AUTHENTICATION & SECURITY LAYER
================================================================================
`backend/app/core/security.py` & `backend/app/api/v1/auth.py`:
- Password hashing: Salted SHA-256 with 100,000 PBKDF2 iterations.
- Token generation: HMAC-SHA256 signature containing `sub`, `role`, and `exp` claims.
- Endpoints:
  - `POST /api/v1/auth/register`: Creates `User` row in SQLite.
  - `POST /api/v1/auth/login`: Validates credentials, returns `{access_token, token_type: "bearer"}`.
  - `GET /api/v1/auth/me`: Resolves current user from `Authorization: Bearer <token>` header.
- Dependency `get_current_user` in `backend/app/api/deps.py` with optional authentication fallback for open studio access.

================================================================================
13. MODEL CONTEXT PROTOCOL (MCP) SERVER
================================================================================
`backend/app/mcp_server/server.py`:
- Implements `FastContractMCPServer`:
  - `list_tools()`:
    1. `evaluate_clause`: inputs `clause_text` (str), `clause_type` (str).
    2. `get_playbook_rules`: inputs `playbook_id` (optional str).
    3. `calculate_risk_matrix`: inputs `flagged_counts` ({critical, high, medium}).
  - `call_tool(tool_name, arguments)`:
    - `evaluate_clause`: Matches domain risk signals ("unlimited", "tipping basket", "without accounting", "immediate termination"). Returns `{clause_type, is_compliant, risk_level, flagged_signals, standard_policy, recommended_action}`.
    - `calculate_risk_matrix`: Computes `score = min(100.0, 35*critical + 20*high + 10*medium)` and returns verdict `"REJECT / REDLINE"` or `"APPROVED WITH CAUTION"`.
- Endpoints in `backend/app/main.py`:
  - `GET /mcp/tools` -> `{"tools": mcp_server.list_tools()}`
  - `POST /mcp/call` -> `{"result": mcp_server.call_tool(name, args)}`

================================================================================
14. TOKEN & COST TELEMETRY ENGINE
================================================================================
`backend/app/core/token_tracker.py`:
- Token Estimation: `max(1, len(text) // 4)`.
- Pricing Table (USD per 1,000 tokens):
  - `gemini-2.0-flash` / `gemini-3.5-flash-lite`: Prompt $0.000075, Completion $0.0003
  - `gpt-4o`: Prompt $0.005, Completion $0.015
  - `claude-3-5-sonnet`: Prompt $0.003, Completion $0.015
  - `deepseek-r1`: Prompt $0.00055, Completion $0.00219
  - `ollama`: $0.00 / $0.00
  - `default`: Prompt $0.002, Completion $0.008
- Method `log_execution(db, contract_id, agent_name, action, prompt_text, completion_text, latency_ms, model_name)`:
  - Calculates cost, inserts `AuditLog` row, commits to DB.
- Telemetry Endpoints:
  - `GET /api/v1/analysis/audit/summary`: Computes total tokens, total USD cost, average latency, and per-agent execution breakdown.
  - `DELETE /api/v1/analysis/audit/reset`: Truncates all `AuditLog` rows.

================================================================================
15. INTERACTIVE REDLINE DECISIONS, AI PROMPT REWRITING & RISK FILTERING
================================================================================
1. Risk-Level & Decision Status Filtering:
   - Endpoint: `GET /api/v1/analysis/{contract_id}/redlines`
   - Query Parameters:
     - `risk_severity`: Optional string (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `ALL`).
     - `decision`: Optional string (`accepted`, `rejected`, `pending`, `ALL`).
   - Filters `contract.redlines` dynamically before returning.

2. Accepting / Rejecting / Resetting Redlines:
   - Endpoint: `PATCH /api/v1/analysis/{contract_id}/redlines/{redline_id}`
   - Request Body: `{"accepted": true | false | null}`
   - Updates target redline record in DB and returns updated redline.

3. AI Prompt Rewriting & Regeneration:
   - Endpoint: `POST /api/v1/analysis/{contract_id}/redlines/{redline_id}/regenerate`
   - Request Body: `{"custom_prompt": str, "provider": Optional[str], "model_name": Optional[str]}`
   - Pipeline:
     1. Loads original clause text and previous suggested text.
     2. Prompts LLM with custom prompt instruction.
     3. Parses structured JSON replacement.
     4. Recomputes word diff tokens via `diff_engine.generate_clause_diff()`.
     5. Resets decision `accepted = None` and updates `custom_prompt`.
     6. Appends a new turn to `contract.debate_transcript` tagged `agent_name: "Client Prompt & Arbiter"`.
     7. Commits to DB and returns updated redline.

================================================================================
16. FASTAPI REST API & SSE STREAMING SPECIFICATION
================================================================================
Expose the complete suite of REST and streaming endpoints:

- Contracts Management:
  - `POST /api/v1/contracts/upload`: Multipart PDF upload, PII redaction, table extraction, ChromaDB indexing, contract row creation.
  - `POST /api/v1/contracts/demo/{sample_type}`: Instant load & auto-analysis of benchmark contracts (`cross_border_ma`, `cloud_ai_dpa`, `ai_joint_rd`, `enterprise_msa`, `saas_agreement`, `mutual_nda`).
  - `GET /api/v1/contracts/`: List all analyzed contracts with pagination (`skip=0&limit=50&status=...`).
  - `GET /api/v1/contracts/{id}`: Full contract detail view.
  - `DELETE /api/v1/contracts/{id}`: Deletes contract row, audit logs, ChromaDB collection, and removes file from disk.
  - `POST /api/v1/contracts/compare`: Side-by-side contract comparison and risk delta.

- Multi-Agent Analysis & Streaming:
  - `POST /api/v1/analysis/{id}/trigger`: Triggers orchestrator graph execution.
  - `GET /api/v1/stream/debate/{contract_id}`: Real-time SSE streaming endpoint (`text/event-stream`).

- Interactive Redlines & Decisions:
  - `GET /api/v1/analysis/{id}/redlines`: List redlines with `risk_severity` and `decision` filters.
  - `PATCH /api/v1/analysis/{id}/redlines/{redline_id}`: Accept/reject/reset a redline.
  - `POST /api/v1/analysis/{id}/redlines/{redline_id}/regenerate`: Rewrites redline via custom prompt.

- Multi-Format Compliance Exports:
  - `GET /api/v1/analysis/{id}/export/docx`: Word (.docx) with authentic Track Changes.
  - `GET /api/v1/analysis/{id}/export/calendar`: RFC 5545 iCalendar (.ics) obligations schedule.
  - `GET /api/v1/analysis/{id}/export/json`: Full audit intelligence JSON dump.
  - `GET /api/v1/analysis/{id}/export/csv`: RFC 4180 tabular CSV matrix.

- Telemetry, Diagnostics & LLM Config:
  - `GET /api/v1/analysis/audit/summary`: Global telemetry summary.
  - `DELETE /api/v1/analysis/audit/reset`: Truncates audit log table.
  - `GET /api/v1/analysis/llm/health`: Multi-provider latency and reachability probe.
  - `GET /api/v1/analysis/llm/config`: Status of provider API keys.
  - `POST /api/v1/analysis/llm/config`: Runtime API key update.

- Playbooks:
  - `GET /api/v1/playbook/list`: Lists built-in playbooks.
  - `GET /api/v1/playbook/custom`: Lists user custom playbooks.
  - `POST /api/v1/playbook/custom`: Creates a custom playbook.
  - `DELETE /api/v1/playbook/custom/{name}`: Deletes a custom playbook.

- Authentication:
  - `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me`.

- Health & Static Serving:
  - `GET /health`: JSON `{"status": "healthy", "version": "1.5.3"}`.
  - `GET /` & `GET /studio`: Serves `backend/static/index.html`.

================================================================================
17. FRONTEND: ALPINE.JS 3.14 & TAILWIND CSS NEO-LEGAL STUDIO
================================================================================
Implement the standalone Neo-Legal Studio in `backend/static/index.html` and mirrored in `frontend/public/index.html`:

- Styling & Typography:
  - Google Fonts: Plus Jakarta Sans (body, headings), JetBrains Mono (badges, metrics, diff tokens).
  - Background: `#F4F6FC` with subtle radial blur gradients.
  - Accents: `#5B67F6`, `#6366F1`.
  - Dark container elements: Slate-900 `#1E2238`.

- UI Architecture & Interactive Components:
  1. Top Navigation Bar:
     - Hamburger toggle opening slide-out system drawer.
     - Brand logo with gradient scale icon and `v1.5.3` badge.
     - View switcher pills: "Ingestion Studio" vs "Telemetry & Audits".
     - Live Engine status pill with pulsating ping dot and active model badge.
     - Settings & API keys modal trigger.

  2. 7-Step Interactive Guided Rundown Tour:
     - Floating question mark (`?`) button with initial pulsating bubble: `"Click here for a rundown"`.
     - When active, screen dims with backdrop blur (`fixed inset-0 bg-slate-950/50`).
     - Targeted element receives `.tour-spotlight-active` with intense pulsating halo:
       `box-shadow: 0 0 0 11px rgba(91, 103, 246, 0.8), 0 0 70px rgba(91, 103, 246, 0.8)`.
     - Step 1: Benchmark Quick-Start Hub
     - Step 2: Custom PDF Upload Dropzone
     - Step 3: Multi-Agent Live Debate Feed
     - Step 4: Interactive Redlines Hub & Risk Filters
     - Step 5: Inline AI Prompt Rewriter
     - Step 6: Multi-Format Compliance Export Suite
     - Step 7: Telemetry & Audits Dashboard

  3. Benchmark Contracts Hub:
     - 6 one-click cards with preset risk badges:
       - Cross-Border M&A (Risk: 87, Tipping baskets & IP trap)
       - Cloud AI & DPA (Risk: 79, Model training on data & SLAs)
       - AI Joint R&D (Risk: 83, Joint IP without accounting)
       - Enterprise MSA (Risk: 65, Uncapped indemnity & caps)
       - SaaS Agreement (Risk: 50, Auto-renewal lock-in)
       - Mutual NDA (Risk: 25, Standard confidentiality)

  4. Live Debate Feed:
     - Server-Sent Events (SSE) listener connected to `/api/v1/stream/debate/{contract_id}`.
     - Avatar badges for Auditor, Opposing Counsel, Redline Synthesizer, and Obligation Extractor.
     - Real-time pulsating indicator while debate is active.

  5. Interactive Redlines Hub:
     - Risk Severity Filter Pills: `All`, `Critical` (red badge), `High` (amber badge), `Medium` (blue badge), and `Low` (slate badge) with reactive count indicators (`countRedlinesByRisk(sev)`).
     - Decision Status Filter Pills: `All`, `Pending` (slate), `Accepted` (green), and `Rejected` (red) with reactive count indicators (`countRedlinesByDecision(dec)`).
     - Live Counter: `"Showing X of Y redlines • Filtered by [Severity] risk • Status: [Decision]"`.
     - Word insertions rendered with `.diff-ins` (emerald background, green text, underline).
     - Word deletions rendered with `.diff-del` (red background, red text, strikethrough).
     - Action Toolbar:
       - **Accept** button: toggles `accepted = true`, calls `PATCH` endpoint, turns solid green.
       - **Reject** button: toggles `accepted = false`, calls `PATCH` endpoint, turns solid red.
       - **Reset** button: clears choice back to pending review.
       - **Rewrite with AI Prompt** button: toggles inline AI prompt rewriter drawer.
     - Inline AI Prompt Rewriter Drawer:
       - Input field bound to `rewritePrompts[rl.id]`.
       - Quick instruction chips:
         - `+ Make Mutual`
         - `+ 1x Annual Cap`
         - `+ 30-Day Cure`
         - `+ Strike AI Training`
       - **Regenerate Redline** button: executes `POST .../regenerate`, triggers spinner, updates diff tokens live.

  6. Multi-Format Compliance Export Suite:
     - Toolbar with 4 dedicated export buttons:
       - **Word DOCX (Track Changes)**: Triggers download of `.docx` reflecting accept/reject decisions.
       - **iCalendar (.ics)**: Triggers download of RFC 5545 compliance calendar.
       - **Full Audit JSON**: Triggers download of structured analysis dump.
       - **Tabular CSV**: Triggers download of CSV matrix.

  7. Side-by-Side Contract Comparison Modal:
     - Selects source and target contract IDs.
     - Displays risk score delta with green/red indicator.
     - Side-by-side section text diff viewer.

  8. LLM Provider Diagnostic Modal:
     - Calls `GET /api/v1/analysis/llm/health`.
     - Displays latency ping for Gemini, Ollama, OpenAI, Anthropic with green/red health badges.

  9. Obligations Matrix:
     - Columns: Citation, Category, Obligor, Recipient, Due Date / Trigger, Recurrence, Penalty for Breach.
     - Critical obligations marked with high-priority alert badges.

  10. Telemetry & Audits Dashboard:
      - KPI cards: Total Tokens Processed, Total Cloud Cost USD, Average Node Latency, Active LLM Core.
      - Execution log table with agent name, prompt/completion tokens, latency, cost, and timestamps.
      - "Reset Metrics" button.

================================================================================
18. DEPLOYMENT & PRODUCTION ORCHESTRATION
================================================================================
1. Local 1-Click Launch:
   - `run_contractmind.bat`: Verifies Python 3.10+, installs requirements, executes `python launch.py`.
   - `launch.py`: Creates storage directories, runs database migrations, launches Uvicorn on `0.0.0.0:8000`, logs to `backend/backend.log`, and opens default browser to `http://localhost:8000`.

2. Vercel Multi-Service Deployment (`vercel.json`):
   - Configures backend service (FastAPI) and frontend service (Next.js).
   - Rewrites API, docs, MCP, static, and health routes to the backend service.
   - Frontend Next.js bridge (`frontend/app/route.ts`) serves identical Alpine.js v1.5.3 Studio.

================================================================================
19. VERIFICATION & AUTOMATED TEST SUITE (16/16 PYTEST SPECIFICATIONS)
================================================================================
The codebase must pass all 16 automated integration tests with zero errors:
1. `backend/tests/test_api_integration.py`:
   - Health check endpoint verification.
   - Demo contract load & analysis execution.
   - Contracts listing and detail verification.
   - DOCX Track Changes export file verification.
   - Audit telemetry summary verification.
2. `backend/tests/test_contractmind.py`:
   - PII redaction accuracy across SSN, email, phone, credit card.
   - PyMuPDF text & Markdown table extraction.
   - Contextual RAG indexing & query retrieval.
   - Word Track Changes low-level XML `<w:ins>` and `<w:del>` verification.
   - MCP tools registration and JSON-RPC execution.
3. `backend/tests/test_v152_features.py`:
   - Redline Accept / Reject PATCH persistence.
   - AI prompt rewriting with diff token recomputation.
   - Risk severity query filtering (`risk_severity=CRITICAL`).
   - Decision status query filtering (`decision=accepted`).
4. `backend/tests/test_v153_enhancements.py`:
   - SSE debate stream connectivity and history replay.
   - iCalendar RFC 5545 (.ics) export formatting and VEVENT attributes.
   - Full audit JSON and CSV matrix export downloads.
   - Side-by-side contract comparison endpoint and risk delta calculation.
   - Custom playbook CRUD operations (`GET`, `POST`, `DELETE`).
   - LLM health probe telemetry (`/api/v1/analysis/llm/health`).
   - User registration and bearer token authentication.
   - Contract deletion with disk file and vector cleanup.
```
