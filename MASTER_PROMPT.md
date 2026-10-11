# 🏛️ ContractMind v1.5.3 — The Ultimate Master Architecture & Reproduction Prompt (A-Z)

> **Document Version:** 1.5.3  
> **Target Project:** ContractMind v1.5.3 (Autonomous Multi-Agent Legal AI Studio)  
> **Track:** JusticeSphere_AI — AI Builders Congress 2026  
> **Repository:** [https://github.com/Faiazzend/JusticeSphereAI](https://github.com/Faiazzend/JusticeSphereAI)

---

```markdown
You are an elite Principal AI Systems Architect, Security Engineer, and Legal Tech Specialist.
Build "ContractMind v1.5.3" completely from scratch: an enterprise-grade, autonomous multi-agent legal intelligence platform that ingests complex commercial contracts, conducts adversarial negotiation debate, synthesizes consensus redlines with authentic Word OpenXML Track Changes, extracts structured obligation matrices, enables live Server-Sent Events (SSE) streaming, provides multi-format compliance exports (Word, RFC 5545 iCalendar .ics, JSON, CSV), compares contracts with risk deltas, manages custom negotiation playbooks, offers multi-provider LLM latency health probes, and features an interactive Alpine.js Neo-Legal Studio with risk-level browsing, lawyer-in-the-loop clause decisions, and AI prompt rewriting.

Implement the system strictly following the exact architectural specifications, database schemas, agent graphs, styling design system, and API protocols specified below. Executing this prompt must produce an exact 1:1 replica of the production live build with zero discrepancies.

================================================================================
TABLE OF CONTENTS
================================================================================
1. High-Level Architecture & Technical Stack
2. Complete Directory Structure & File Hierarchy
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
17. Frontend: Alpine.js 3.14 & Tailwind CSS Neo-Legal Studio (Full UI Architecture)
18. Next.js Bridge, Deployment & Production Orchestration (Local & Vercel Multi-Service)
19. Benchmark Sample Contract Definitions (sample_contracts/)
20. Verification & Automated Test Suite (16/16 Pytest Specifications)

================================================================================
1. HIGH-LEVEL ARCHITECTURE & TECHNICAL STACK
================================================================================
- Backend Framework: FastAPI (Python 3.10+) with async endpoints, lifespan DB initialization, and CORS middleware configured for full client origin access.
- Database: SQLite with async SQLAlchemy 2.0 (aiosqlite). Dynamic database path resolves to /tmp/contractmind.db if VERCEL=1 is detected.
- Vector Engine: ChromaDB persistent client with automatic fallback to in-memory term-frequency cosine scorer.
- Document Processing: PyMuPDF (fitz) for text extraction, native PDF table detection converted to Markdown tables, and regex-based PII redaction.
- Agent Architecture: StateGraph pattern with 4 specialized roles:
  1. Auditor Agent (Policy defender, scans 10 risk categories with regex, LLM statement generation, token & latency logging).
  2. Opposing Counsel Agent (Counterparty negotiator, aggressive commercial defense, compromise proposal).
  3. Redline Synthesizer Agent (Consensus arbiter, word-level SequenceMatcher diff tokens, composite risk scoring).
  4. Obligation Extractor Agent (Calendar extractor, role matrix, penalty monitor, extracts 10 obligation patterns).
- Resilience & Event Broadcasting:
  - Per-node failure isolation: each graph node wrapped in try/except; on exception, node logs error, records fallback turn in debate transcript, and allows subsequent nodes to proceed.
  - EventBroadcaster: in-memory pub/sub publishing agent lifecycle events to async queues for real-time SSE streaming.
- Real-Time Live Streaming:
  - Server-Sent Events (SSE) endpoint at `/api/v1/stream/{id}` and `/api/v1/stream/debate/{id}` with standard headers (`Cache-Control: no-cache`, `X-Accel-Buffering: no`), replaying history for completed contracts, streaming live node events, and periodic `: ping\n\n` comments.
- Word Track Changes (.docx):
  - python-docx with custom OpenXML manipulation injecting low-level `<w:ins>` and `<w:del>` elements with author attribution and UTC timestamps.
  - Decision branching: Accepted/Pending redlines include tracked changes; Rejected redlines retain original clause cleanly.
  - Non-blocking execution via `asyncio.to_thread`.
- Multi-Format Export Suite:
  - Word (.docx) with authentic Track Changes.
  - iCalendar (.ics) RFC 5545 compliance calendar with VEVENT entries for deadlines (accessible via `/export/ics` and `/export/calendar`).
  - Audit JSON (.json) complete contract intelligence dump.
  - Tabular CSV (.csv) RFC 4180 obligations and redlines matrix.
- Contract Comparison:
  - Side-by-side section comparison diffing text tokens and calculating overall risk score delta, accepting either `base_contract_id` or `source_contract_id`.
- Custom Playbooks:
  - CRUD API managing custom institutional negotiation policies alongside built-in standard playbooks, with flexible schemas and auto-generated IDs.
- LLM Gateway & Health Telemetry:
  - Google Gemini default core (gemini-2.0-flash / gemini-1.5-flash / gemini-3.5-flash-lite), Ollama local core (qwen3.5:4b), OpenAI (gpt-4o), Anthropic (claude-3-5-sonnet).
  - 60-second timeouts, 4096 maxOutputTokens.
  - Real-time provider health diagnostic endpoint (`/api/v1/analysis/llm/health`).
  - High-fidelity deterministic legal fallback simulator if network or API keys are unavailable.
- User Authentication:
  - Salted SHA-256 password hashing, HMAC bearer tokens, register/login/me endpoints with User model (`id`, `email`, `hashed_password`, `full_name`, `role`, `is_active`).
- Protocol: Model Context Protocol (MCP) JSON-RPC tools gateway at `/mcp/tools` and `/mcp/call`.
- Frontend: Single-Page Application (SPA) built using Alpine.js 3.14, Tailwind CSS, FontAwesome 6, Plus Jakarta Sans, and JetBrains Mono. Dual-served via FastAPI (`backend/static/index.html`) and Next.js 14 bridge (`frontend/public/index.html` + `frontend/app/route.ts`).
  - Features a 7-step guided rundown tour with high-intensity glowing halo spotlights (`#5B67F6`).
  - Redline risk-level filtering (Critical, High, Medium, Low) and decision status filtering (Pending, Accepted, Rejected) with reactive count badges.
  - Inline Accept / Reject / Reset buttons and inline AI prompt rewriter with quick chips (`+ Make Mutual`, `+ 1x Annual Cap`, `+ 30-Day Cure`, `+ Strike AI Training`).
  - Side-by-side contract comparison view and LLM health diagnostic modal.

================================================================================
2. COMPLETE DIRECTORY STRUCTURE & FILE HIERARCHY
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

Dependencies (`backend/requirements.txt`):
```
fastapi>=0.110.0
uvicorn>=0.28.0
sqlalchemy>=2.0.0
aiosqlite>=0.19.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
pymupdf>=1.24.0
python-docx>=1.1.0
httpx>=0.27.0
aiofiles>=23.2.0
python-multipart>=0.0.9
python-dotenv>=1.0.0
chromadb>=0.4.24
```

Dependencies (`frontend/package.json`):
```json
{
  "name": "contractmind-frontend",
  "version": "1.5.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.2.15",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/node": "^20.14.0",
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "typescript": "^5.4.5"
  }
}
```

================================================================================
3. DATABASE MODELS & SCHEMA SPECIFICATIONS
================================================================================
Implement async SQLAlchemy 2.0 models using `DeclarativeBase`:

1. `Contract` (`backend/app/models/contract.py`):
   - Table: `"contracts"`
   - `id`: String(36), primary key (UUID default: `lambda: str(uuid.uuid4())`).
   - `title`: String(255), default="Untitled Contract".
   - `original_filename`: String(255), default="contract.pdf".
   - `file_path`: String(512), default="".
   - `status`: String(50), default="uploaded" ("uploaded", "processing", "analyzed", "error").
   - `overall_risk_score`: Float, default=0.0.
   - `raw_text`: Text, default="".
   - `playbook_name`: String(100), default="Standard Corporate Playbook".
   - `extracted_sections`: JSON, default=list (items: `{section_number, title, content, page_number}`).
   - `identified_risks`: JSON, default=list (items: `{id, category, severity, score, clause_reference, original_text, legal_rationale, mitigation_strategy}`).
   - `debate_transcript`: JSON, default=list (items: `{agent_name, timestamp, content, target_clause}`).
   - `redlines`: JSON, default=list (items: `{id, section_number, original_text, suggested_text, diff_type, risk_severity, legal_rationale, diff_tokens, accepted, custom_prompt}`).
   - `obligations`: JSON, default=list (items: `{id, clause_reference, obligor, recipient, obligation_type, description, due_date_or_trigger, recurrence, penalty_for_breach, is_critical}`).
   - `risk_summary`: JSON, default=`{"critical": 0, "high": 0, "medium": 0, "low": 0}`.
   - `created_at`: DateTime(timezone=True), default=`lambda: datetime.now(timezone.utc)`.
   - `updated_at`: DateTime(timezone=True), default=`lambda: datetime.now(timezone.utc)`, onupdate=`lambda: datetime.now(timezone.utc)`.
   - `audit_logs`: Relationship to `AuditLog`, back_populates="contract", cascade="all, delete-orphan".

2. `AuditLog` (`backend/app/models/audit.py`):
   - Table: `"audit_logs"`
   - `id`: Integer, primary key, autoincrement=True.
   - `contract_id`: String(36), ForeignKey("contracts.id", ondelete="CASCADE"), nullable=True.
   - `agent_name`: String(100), nullable=False.
   - `action`: String(100), nullable=False.
   - `prompt_tokens`: Integer, default=0.
   - `completion_tokens`: Integer, default=0.
   - `total_tokens`: Integer, default=0.
   - `latency_ms`: Float, default=0.0.
   - `model_name`: String(100), default="fallback-simulator".
   - `estimated_cost_usd`: Float, default=0.0 (precision 6 decimal places).
   - `details`: Text, nullable=True.
   - `created_at`: DateTime(timezone=True), default=`lambda: datetime.now(timezone.utc)`.
   - `contract`: Relationship to `Contract`, back_populates="audit_logs".

3. `User` (`backend/app/models/user.py`):
   - Table: `"users"`
   - `id`: String(36), primary key (UUID default: `lambda: str(uuid.uuid4())`).
   - `email`: String(255), unique=True, index=True, nullable=False.
   - `hashed_password`: String(255), default="".
   - `full_name`: String(255), default="Counsel Member".
   - `role`: String(50), default="lawyer".
   - `is_active`: Boolean, default=True.
   - `created_at`: DateTime(timezone=True), default=`lambda: datetime.now(timezone.utc)`.

================================================================================
4. PDF INGESTION, TABLE EXTRACTION & PII REDACTION ENGINE
================================================================================
1. `backend/app/core/pii_redactor.py`:
   - Compiled regex patterns:
     - SSN: `r"\b\d{3}-\d{2}-\d{4}\b"`
     - Credit Card: `r"\b(?:\d{4}[-\s]?){3}\d{4}\b"`
     - Email: `r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"`
     - Phone: `r"\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b"`
     - Bank Account: `r"\b\d{8,17}\b"`
     - Tax ID: `r"\b\d{2}-\d{7}\b"`
   - Method `redact(text: str) -> Tuple[str, Dict[str, int]]`:
     Replaces matches with `[REDACTED_{TYPE}]`, counting instances per type.

2. `backend/app/services/pdf_processor.py`:
   - Uses PyMuPDF (`fitz`).
   - `process_pdf(file_path: str) -> Tuple[str, List[Dict[str, Any]]]`:
     - Reads pages, extracts raw text via `page.get_text("text")`.
     - Detects tabular exhibits via `page.find_tables()`. Converts table matrices into clean Markdown format via helper:
       `[TABLE EXHIBIT - Page {p}]\n| col1 | col2 |\n| --- | --- |\n| val1 | val2 |`
     - Concatenates full text and applies `pii_redactor.redact()`.
     - Segments text into structured sections using section header regex:
       `r"(?:\n|^)(?:SECTION|ARTICLE|CLAUSE)?\s*(\d+(?:\.\d+)*|[IVXLCDM]+)[\.\:\-\s]+([A-Z][A-Za-z0-9\s\,\-\&\/\(\)]+)(?=\n)"`
     - If fewer than 2 headers matched, falls back to paragraph/block chunking.
     - Returns `(clean_text, sections)`.

================================================================================
5. CONTEXTUAL RAG & SEMANTIC CHUNKING ENGINE
================================================================================
`backend/app/services/rag_engine.py`:
- Contextual Semantic Chunking:
  - If a section's content > 1500 characters, splits along paragraph boundaries.
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
  - `sections`: List[Dict[str, Any]]
  - `playbook_rules`: List[Dict[str, Any]]
  - `debate_cycle`: int
  - `max_debate_cycles`: int
  - `use_local_llm`: bool
  - `llm_provider`: Optional[str]
  - `model_name`: Optional[str]
  - `api_key_override`: Optional[str]
  - `identified_risks`: List[Dict[str, Any]]
  - `debate_transcript`: List[Dict[str, Any]]
  - `redlines`: List[Dict[str, Any]]
  - `obligations`: List[Dict[str, Any]]
  - `risk_summary`: Dict[str, int]
  - `overall_score`: float
  - `current_status`: str
  - `error`: Optional[str]

`backend/app/agents/graph.py` & Agent Nodes:
1. `EventBroadcaster`:
   - Singleton broadcaster maintaining `self._subscribers: Dict[str, List[asyncio.Queue]]`.
   - `subscribe(contract_id) -> asyncio.Queue`, `unsubscribe(contract_id, queue)`, `broadcast(contract_id, event_dict)`.

2. Sequential Pipeline with Per-Node Failure Isolation:
   - Helper `_run_node_safely(node_fn, name, current_state)`:
     Broadcasts `agent_started`, executes node inside `try ... except`. On exception, logs error, appends a fallback turn to `debate_transcript` tagged `"{name} (Resilience Guard)"`, broadcasts `agent_warning`, and passes state to the next node.

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
     - Prompts LLM or uses deterministic legal fallback responses per category.
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
  - Returns:
    ```json
    {
      "status": "healthy",
      "active_provider": "gemini",
      "providers": {
        "gemini": { "available": true, "latency_ms": 312.4, "message": "Ready" },
        "ollama": { "available": false, "latency_ms": 0.0, "message": "No local Ollama server responding on port 11434" },
        "openai": { "available": false, "latency_ms": 0.0, "message": "OPENAI_API_KEY not configured" },
        "anthropic": { "available": false, "latency_ms": 0.0, "message": "ANTHROPIC_API_KEY not configured" },
        "fallback-simulator": { "available": true, "latency_ms": 1.1, "message": "Deterministic Neo-Legal Heuristic Core active (100% SLA)" }
      }
    }
    ```

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
      containing `<w:r>`, `<w:rPr><w:strike/><w:color w:val="DC2626"/></w:rPr>`, and `<w:delText xml:space="preserve">{text}</w:delText>`.
    - Insertion: `<w:ins w:id="{id}" w:author="ContractMind Legal AI" w:date="{utc_now}">`
      containing `<w:r>`, `<w:rPr><w:u w:val="single"/><w:color w:val="16A34A"/></w:rPr>`, and `<w:t xml:space="preserve">{text}</w:t>`.
  - Section 1: Executive Risk & Scorecard Summary Table:
    - Lists Composite Risk Score, Critical Count, High Count, Medium Count, Low Count.
  - Section 2: Redline Decisions Overview Table:
    - Lists Section, Severity, Redline Type, Decision Status ("Accepted", "Rejected", or "Pending Review").
  - Section 3: Detailed Proposed Contract Redlines (Track Changes):
    - Heading: `Section {sec_num} [Severity: {severity} | Decision: {status_text}]`.
    - If `accepted is False` (Rejected):
      Adds bold indicator `Decision: REJECTED (Original Clause Retained):` and outputs clean original clause text.
    - If `accepted is True` or `None` (Accepted or Pending Review):
      Adds bold indicator `Decision: {STATUS} (Track Changes XML Enabled):` and appends native `<w:ins>` and `<w:del>` XML runs to `paragraph._p`.
  - Section 4: Extracted Contractual Obligations & Compliance Calendar Table:
    - Lists Citation / Type, Obligor, Recipient, Trigger / Deadline, Criticality, Breach Penalty.
- Non-blocking execution: File creation and I/O wrapped in `asyncio.to_thread()` in `api/v1/analysis.py`.

================================================================================
9. MULTI-FORMAT LEGAL EXPORT SUITE (DOCX, ICALENDAR, JSON, CSV)
================================================================================
Expose 4 dedicated compliance export endpoints in `backend/app/api/v1/analysis.py`:

1. Word Track Changes (.docx):
   - Endpoint: `GET /api/v1/analysis/{id}/export/docx`
   - Content-Type: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
   - Header: `Content-Disposition: attachment; filename="{title}_redlines.docx"`

2. iCalendar RFC 5545 Compliance Schedule (.ics):
   - Endpoints: `GET /api/v1/analysis/{id}/export/ics` AND `GET /api/v1/analysis/{id}/export/calendar`
   - Content-Type: `text/calendar; charset=utf-8`
   - Header: `Content-Disposition: attachment; filename="{title}_obligations.ics"`
   - Emits RFC 5545 calendar with `BEGIN:VCALENDAR`, `VERSION:2.0`, `PRODID:-//ContractMind//Legal Obligation Calendar v1.5.3//EN`.
   - Each obligation emits a `BEGIN:VEVENT`:
     - `UID`: `{contract_id}_{obligation_id}@contractmind.ai`
     - `DTSTAMP`: UTC timestamp now (`%Y%m%dT%H%M%SZ`).
     - `DTSTART`: Due date or trigger calculated stamp.
     - `SUMMARY`: `[{category}] {obligor} -> {recipient}`
     - `DESCRIPTION`: Full description with breach penalty.
     - `PRIORITY`: `1` if critical, `5` otherwise.

3. Complete Audit JSON Dump (.json):
   - Endpoint: `GET /api/v1/analysis/{id}/export/json`
   - Content-Type: `application/json`
   - Header: `Content-Disposition: attachment; filename="{title}_audit_dump.json"`
   - Returns full contract record, extracted sections, identified risks, debate transcript, redlines with decisions, obligations matrix, and risk summary.

4. Tabular CSV Matrix (.csv):
   - Endpoint: `GET /api/v1/analysis/{id}/export/csv`
   - Content-Type: `text/csv; charset=utf-8`
   - Header: `Content-Disposition: attachment; filename="{title}_matrix.csv"`
   - Generates two sections formatted per RFC 4180:
     - Section 1: `=== REDLINES & NEGOTIATION RECOMMENDATIONS ===`
       Headers: `ID, Section, Severity, Diff Type, Decision Status, Legal Rationale, Original Text, Suggested Text`
     - Section 2: `=== EXTRACTED OBLIGATIONS & COVENANTS ===`
       Headers: `Obligor, Recipient, Due Date / Trigger, Criticality, Breach Penalty, Summary`

================================================================================
10. CONTRACT COMPARISON & RISK DELTA ENGINE
================================================================================
`backend/app/api/v1/contracts.py`:
- Endpoint: `POST /api/v1/contracts/compare`
- Request Schema (`ContractCompareRequest`):
  ```python
  class ContractCompareRequest(BaseModel):
      base_contract_id: Optional[str] = None
      source_contract_id: Optional[str] = None
      target_contract_id: str

      @model_validator(mode="after")
      def resolve_base_id(self):
          if not self.base_contract_id and not self.source_contract_id:
              raise ValueError("Either base_contract_id or source_contract_id must be provided")
          if not self.base_contract_id:
              self.base_contract_id = self.source_contract_id
          return self
  ```
- Response Schema (`ContractCompareResponse`):
  ```python
  class SectionDiffItem(BaseModel):
      section_title: str
      status: str
      diff_tokens: List[Dict[str, str]]

  class ContractCompareResponse(BaseModel):
      base_id: str
      base_title: str
      target_id: str
      target_title: str
      base_risk_score: float
      target_risk_score: float
      risk_score_delta: float
      sections: List[SectionDiffItem]
      source_id: Optional[str] = None
      source_title: Optional[str] = None
      source_risk_score: Optional[float] = None
      risk_delta: Optional[float] = None
  ```
- Logic: Matches sections by title or number, runs `diff_engine.generate_clause_diff()`, and computes `risk_delta = round(target.overall_risk_score - base.overall_risk_score, 2)`.

================================================================================
11. CUSTOM PLAYBOOK MANAGEMENT SYSTEM (CRUD API)
================================================================================
`backend/app/api/v1/playbook.py`:
- Schemas (`app/schemas/playbook_schemas.py`):
  ```python
  class PlaybookRule(BaseModel):
      category: str
      severity: Optional[str] = "HIGH"
      preferred_position: Optional[str] = ""
      fallback_position: Optional[str] = ""
      hard_stop: Optional[str] = ""
      rule_id: Optional[str] = None
      standard_position: Optional[str] = None

  class Playbook(BaseModel):
      id: Optional[str] = None
      name: str
      description: str
      rules: List[PlaybookRule] = Field(default_factory=list)
      risk_tolerance: Optional[float] = None

      @model_validator(mode="after")
      def ensure_id(self):
          if not self.id:
              self.id = self.name.lower().replace(" ", "_").replace("-", "_")
          return self
  ```
- Endpoints:
  - `GET /api/v1/playbook/list`: Returns built-in standard playbooks (`Strict Enterprise`, `Standard Corporate`, `Founder Friendly`, `M&A Aggressive`).
  - `GET /api/v1/playbook/custom`: Lists user custom playbooks from `CUSTOM_PLAYBOOKS` dictionary.
  - `POST /api/v1/playbook/custom`: Creates or updates custom playbook in memory.
  - `DELETE /api/v1/playbook/custom/{id}`: Deletes custom playbook.
  - `GET /api/v1/playbook/{id}`: Retrieves specific playbook by ID or name.

================================================================================
12. USER AUTHENTICATION & SECURITY LAYER
================================================================================
`backend/app/core/security.py` & `backend/app/api/v1/auth.py`:
- Password Hashing: Salted SHA-256 (`secrets.token_hex(16)` + `hashlib.sha256`) returning `"{salt}${hash}"`.
- Bearer Tokens: Signed token format `"{subject}:{expires_timestamp}:{hmac_signature}"` using `hmac.new(b"contractmind-secret-key-2026", ...)`.
- Endpoints:
  - `POST /api/v1/auth/register`:
    - Body: `{"email": EmailStr, "password": str, "full_name": str, "role": str = "reviewer"}`
    - Creates `User` row, returns `TokenResponse(access_token, token_type="bearer", user_id, email, role)`.
  - `POST /api/v1/auth/login`:
    - Body: `{"email": EmailStr, "password": str}`
    - Verifies password hash, returns `TokenResponse`.
  - `GET /api/v1/auth/me`: Resolves current user from `Authorization: Bearer <token>` header.

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
  - `GET /api/v1/analysis/audit/summary`: Computes `total_tokens`, `total_cost_usd`, `avg_latency_ms`, `total_runs`, and `by_agent` breakdown.
  - `DELETE /api/v1/analysis/audit/reset`: Truncates all `AuditLog` rows.

================================================================================
15. INTERACTIVE REDLINE DECISIONS, AI PROMPT REWRITING & RISK FILTERING
================================================================================
1. Risk-Level & Decision Status Filtering:
   - Endpoint: `GET /api/v1/analysis/{id}/redlines`
   - Query Parameters:
     - `risk_severity`: Optional string (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `ALL`).
     - `decision`: Optional string (`accepted`, `rejected`, `pending`, `ALL`).
   - Filters `contract.redlines` dynamically before returning.

2. Accepting / Rejecting / Resetting Redlines:
   - Endpoint: `PATCH /api/v1/analysis/{id}/redlines/{redline_id}`
   - Request Body: `{"accepted": true | false | null}`
   - Updates target redline record in DB and returns updated `RedlineItem`.

3. AI Prompt Rewriting & Regeneration:
   - Endpoint: `POST /api/v1/analysis/{id}/redlines/{redline_id}/regenerate`
   - Request Body: `{"custom_prompt": str, "provider": Optional[str], "model_name": Optional[str]}`
   - Pipeline:
     1. Loads original clause text and previous suggested text.
     2. Prompts LLM with custom prompt instruction:
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
     5. Resets decision `accepted = None` and updates `custom_prompt`.
     6. Appends a new turn to `contract.debate_transcript` tagged `agent_name: "Client Prompt & Arbiter"`.
     7. Commits to DB and returns updated redline.

================================================================================
16. FASTAPI REST API & SSE STREAMING SPECIFICATION
================================================================================
Expose the complete suite of REST and streaming endpoints:

- Contracts Management:
  - `POST /api/v1/contracts/upload`: Multipart PDF upload (`file: UploadFile = File(...)`, `playbook_name: str = Form(...)`).
  - `POST /api/v1/contracts/demo/{sample_type}`: Instant load & auto-analysis of benchmark contracts. Accepts both short and full alias keys:
    - `"ma"` or `"cross_border_ma"` -> Cross-Border Tech M&A Agreement
    - `"cloud_dpa"` or `"cloud_ai_dpa"` -> Enterprise Cloud & AI Data Processing Agreement
    - `"joint_ip"` or `"ai_joint_rd"` -> Autonomous AI Joint R&D & IP License
    - `"msa"` or `"enterprise_msa"` -> Master Services Agreement (MSA)
    - `"saas"` or `"saas_agreement"` -> Enterprise SaaS Subscription Agreement
    - `"nda"` or `"mutual_nda"` -> Mutual Non-Disclosure Agreement
  - `GET /api/v1/contracts/`: List analyzed contracts with pagination (`skip: int = 0`, `limit: int = 50`, `status: Optional[str] = None`).
  - `GET /api/v1/contracts/{id}`: Full contract detail view (`ContractDetailResponse`).
  - `DELETE /api/v1/contracts/{id}`: Deletes contract row, cascades to audit logs, deletes ChromaDB collection, and removes file from disk.
  - `POST /api/v1/contracts/compare`: Side-by-side contract comparison and risk delta.

- Multi-Agent Analysis & Streaming:
  - `POST /api/v1/analysis/{id}/trigger`: Triggers orchestrator graph execution (`AnalysisTriggerRequest`).
  - `GET /api/v1/stream/{id}` & `GET /api/v1/stream/debate/{id}`: Real-time SSE streaming endpoint (`text/event-stream`).

- Interactive Redlines & Decisions:
  - `GET /api/v1/analysis/{id}/redlines`: List redlines with `risk_severity` and `decision` filters.
  - `PATCH /api/v1/analysis/{id}/redlines/{redline_id}`: Accept/reject/reset a redline (`{"accepted": bool | null}`).
  - `POST /api/v1/analysis/{id}/redlines/{redline_id}/regenerate`: Rewrites redline via custom prompt.

- Multi-Format Compliance Exports:
  - `GET /api/v1/analysis/{id}/export/docx`: Word (.docx) with authentic Track Changes.
  - `GET /api/v1/analysis/{id}/export/ics` & `GET /api/v1/analysis/{id}/export/calendar`: RFC 5545 iCalendar (.ics) obligations schedule.
  - `GET /api/v1/analysis/{id}/export/json`: Full audit intelligence JSON dump.
  - `GET /api/v1/analysis/{id}/export/csv`: RFC 4180 tabular CSV matrix.

- Telemetry, Diagnostics & LLM Config:
  - `GET /api/v1/analysis/audit/summary`: Global telemetry summary (`AuditSummaryResponse`).
  - `DELETE /api/v1/analysis/audit/reset`: Truncates audit log table.
  - `GET /api/v1/analysis/llm/health`: Multi-provider latency and reachability probe (`LLMHealthResponse`).
  - `GET /api/v1/analysis/llm/config`: Status of provider API keys (`LLMConfigResponse`).
  - `POST /api/v1/analysis/llm/config`: Runtime API key update (`LLMConfigUpdateRequest`).

- Playbooks:
  - `GET /api/v1/playbook/list`: Lists built-in playbooks.
  - `GET /api/v1/playbook/custom`: Lists user custom playbooks.
  - `POST /api/v1/playbook/custom`: Creates a custom playbook.
  - `DELETE /api/v1/playbook/custom/{id}`: Deletes a custom playbook.
  - `GET /api/v1/playbook/{id}`: Retrieves specific playbook.

- Authentication:
  - `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me`.

- Health & Static Serving:
  - `GET /health`: JSON `{"status": "healthy", "version": "1.5.3"}`.
  - `GET /` & `GET /studio`: Serves `backend/static/index.html`.

================================================================================
17. FRONTEND: ALPINE.JS 3.14 & TAILWIND CSS NEO-LEGAL STUDIO
================================================================================
Implement the standalone Neo-Legal Studio in `backend/static/index.html` and mirrored in `frontend/public/index.html`:

- Styling & Design Tokens:
  - CSS CDN: Tailwind CSS, FontAwesome 6 Pro/Free, Google Fonts (Plus Jakarta Sans & JetBrains Mono).
  - Background: `#F4F6FC` with subtle radial blur gradients.
  - Brand accents: `#5B67F6`, `#6366F1`.
  - Diff tokens:
    - `.diff-ins`: Emerald background (`#DCFCE7`), emerald text (`#16A34A`), underline.
    - `.diff-del`: Rose background (`#FEE2E2`), rose text (`#DC2626`), strikethrough.
  - Spotlight tour animation:
    ```css
    .tour-spotlight-active {
      position: relative !important;
      z-index: 9999 !important;
      border-radius: 1rem !important;
      box-shadow: 0 0 0 11px rgba(91, 103, 246, 0.8), 0 0 70px rgba(91, 103, 246, 0.8) !important;
      animation: tour-pulse 1.8s infinite ease-in-out;
    }
    @keyframes tour-pulse {
      0%, 100% { box-shadow: 0 0 0 11px rgba(91, 103, 246, 0.8), 0 0 70px rgba(91, 103, 246, 0.8); }
      50% { box-shadow: 0 0 0 18px rgba(91, 103, 246, 0.95), 0 0 100px rgba(91, 103, 246, 1); }
    }
    ```

- Alpine.js State (`contractMindStudio()`):
  - `contracts: []`
  - `selectedContract: null`
  - `currentView: 'studio'` ('studio', 'telemetry', 'compare')
  - `activeProvider: 'gemini'`
  - `selectedPlaybook: 'Standard Corporate Playbook'`
  - `activeRiskFilter: 'ALL'`
  - `activeDecisionFilter: 'ALL'`
  - `rewritePrompts: {}`
  - `rewritePanels: {}`
  - `isRegenerating: {}`
  - `compareBaseId: ''`
  - `compareTargetId: ''`
  - `compareResult: null`
  - `isComparing: false`
  - `tourActive: false`
  - `tourStep: 1`
  - `auditSummary: null`
  - `llmHealth: null`

- Core Reactive Methods:
  - `init()`: Loads contracts list, audit summary, and LLM health probes.
  - `triggerDemo(type)`: POSTs to `/api/v1/contracts/demo/{type}`, sets `selectedContract`, syncs redline panels, and reloads contracts.
  - `selectContract(c)`: Sets active contract, synchronizes rewrite panels.
  - `countRedlinesByRisk(sev)`: Computes count of redlines matching risk severity.
  - `countRedlinesByDecision(dec)`: Computes count of redlines matching decision status.
  - `filteredRedlines()`: Filters redlines based on `activeRiskFilter` and `activeDecisionFilter`.
  - `patchRedlineDecision(contractId, redlineId, accepted)`: Sends `PATCH` request to `/api/v1/analysis/{contractId}/redlines/{redlineId}` with `{"accepted": accepted}`, updating the local state reactively.
  - `regenerateRedline(contractId, redlineId)`: Sends `POST` request to `/api/v1/analysis/{contractId}/redlines/{redlineId}/regenerate` with `{"custom_prompt": prompt}`, replacing diff tokens and legal rationale live.
  - `exportDocx()`, `exportIcs()`, `exportJson()`, `exportCsv()`: Downloads corresponding export files for the currently selected contract.
  - `compareContractsAction()`: Sends `POST` to `/api/v1/contracts/compare` with `{"base_contract_id": compareBaseId, "target_contract_id": compareTargetId}` and populates `compareResult`.
  - `fetchLLMHealth()`: Calls `/api/v1/analysis/llm/health` and displays the diagnostic modal.
  - `resetAuditMetrics()`: Calls `DELETE /api/v1/analysis/audit/reset`.
  - `startTour()`, `nextTour()`, `prevTour()`, `stopTour()`: Manages 7-step guided rundown walkthrough with halo spotlights.

================================================================================
18. NEXT.JS BRIDGE, DEPLOYMENT & PRODUCTION ORCHESTRATION
================================================================================
1. Local 1-Click Launch:
   - `run_contractmind.bat`: Verifies Python 3.10+, installs requirements, executes `python launch.py`.
   - `launch.py`:
     ```python
     import os, sys, asyncio, logging, threading, webbrowser
     from pathlib import Path

     BASE_DIR = Path(__file__).resolve().parent
     BACKEND_DIR = BASE_DIR / "backend"
     sys.path.insert(0, str(BACKEND_DIR))

     from app.config import settings
     from app.database import init_db

     def setup_environment():
         settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
         settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
         settings.EXPORT_DIR.mkdir(parents=True, exist_ok=True)
         settings.CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)

     def main():
         setup_environment()
         asyncio.run(init_db())
         timer = threading.Timer(1.5, lambda: webbrowser.open("http://localhost:8000"))
         timer.daemon = True
         timer.start()
         import uvicorn
         uvicorn.run("app.main:app", host="0.0.0.0", port=8000, app_dir=str(BACKEND_DIR), reload=False)

     if __name__ == "__main__":
         main()
     ```

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

3. Frontend Next.js Bridge (`frontend/app/route.ts` & `frontend/next.config.js`):
   - `frontend/app/route.ts` dynamically serves `frontend/public/index.html` with `Content-Type: text/html; charset=utf-8`.
   - `frontend/next.config.js` redirects `/audit` and `/contracts/*` to `/`, and rewrites `/api/v1/*`, `/health`, and `/mcp/*` to `BACKEND_URL`.

================================================================================
19. BENCHMARK SAMPLE CONTRACT DEFINITIONS (sample_contracts/)
================================================================================
Create the following benchmark sample files in `sample_contracts/`:

1. `sample_contracts/cross_border_ma.txt`:
```
SECTION 1. DEFINITIONS AND CLOSING TERMS
1.1 Working Capital Statement. Within ninety (90) days following the Closing Date, Buyer shall prepare and deliver the final Working Capital Statement. If the Net Working Capital is less than the Target Working Capital, Seller shall promptly forfeit indemnity escrow reserves.

SECTION 2. INDEMNIFICATION AND BASKETS
2.1 Tipping Basket. Seller shall indemnify, defend, and hold harmless Buyer from and against all Losses arising from breaches of Seller Representations; provided, however, that Buyer shall not be entitled to indemnification until aggregate Losses exceed the de minimis threshold of $150,000, whereupon Seller shall be liable for all Losses from dollar one (first-dollar tipping basket), without any aggregate liability super-cap.

SECTION 3. REPRESENTATIONS AND WARRANTIES
3.1 Non-Infringement. To the actual knowledge of the chief executive officer of Seller, without any duty of reasonable inquiry or patent clearance review, Seller does not warrant that its software products infringe or misappropriate any third-party intellectual property or trade secrets.

SECTION 4. ESCROW AND OPERATIONAL COVENANTS
4.1 Earn-Out Discretion. During the Earn-Out Period, Buyer shall exercise unfettered operational discretion over the acquired business, and technology escrow release conditions shall be subject to Buyer's sole approval.

SECTION 5. GOVERNING LAW AND DISPUTE RESOLUTION
5.1 Venue. This Agreement and any dispute hereunder shall be governed exclusively by the substantive laws of Switzerland, and shall be submitted to the ICC rules of arbitration in Geneva, Switzerland.
```

2. `sample_contracts/cloud_ai_dpa.txt`:
```
SECTION 1. SCOPE AND DATA PROCESSING
1.1 Ingestion and Model Training. Customer hereby grants Cloud Provider a perpetual, worldwide license to ingest, de-identify, and utilize Customer Data, Prompts, and Model Outputs to train, fine-tune, and improve foundational AI models and neural model checkpoints.

SECTION 2. SUB-PROCESSORS AND PRIVACY
2.1 Sub-Processor Discretion. Cloud Provider may appoint third-party sub-processors without prior notice to Customer. In the event of a security incident or data breach, Cloud Provider shall notify Customer within forty-eight (48) hours of confirmation.

SECTION 3. SERVICE LEVEL AGREEMENT AND REMEDIES
3.1 Monthly Uptime. Cloud Provider shall target a monthly uptime of 99.5%. In the event uptime falls below this threshold, service credit remittance shall be Customer's sole and exclusive financial remedy.

SECTION 4. DATA DESTRUCTION UPON TERMINATION
4.1 Sanitization. Following termination, Customer may request data destruction, and Provider shall delete customer data within sixty (60) days in accordance with standard internal routines.
```

3. `sample_contracts/ai_joint_rd.txt`:
```
SECTION 1. FOREGROUND INTELLECTUAL PROPERTY
1.1 Joint Ownership. All Foreground Inventions, Model Weights, and Source Code developed jointly by Developer and Sponsor shall be owned jointly by Developer and Sponsor, without obtaining the consent of, or accounting to, the other party for licensing or commercialization anywhere in the world.

SECTION 2. RESTRICTIVE COVENANTS
2.1 Non-Competition. Neither party shall directly or indirectly develop, sell, or commercialize competing foundational AI architectures for a period of five (5) consecutive years following the expiration of this Agreement.
```

4. `sample_contracts/enterprise_msa.txt`:
```
SECTION 1. FEES AND PAYMENT TERMS
1.1 Invoicing. Customer shall remit payment within sixty (60) days of receipt of invoice. Late payments shall incur interest at 1.5% per month.

SECTION 2. LIMITATION OF LIABILITY
2.1 Aggregate Cap. In no event shall either party's aggregate liability exceed the total fees paid by Customer under this Agreement in the preceding six (6) months; provided, however, that Customer's indemnity obligations shall be entirely uncapped.
```

5. `sample_contracts/saas_agreement.txt`:
```
SECTION 1. SUBSCRIPTION TERM AND RENEWAL
1.1 Auto-Renewal. This Agreement shall automatically renew for successive two (2) year terms unless Customer provides written notice of non-renewal at least ninety (90) days prior to expiration. Fees shall automatically escalate by 10% upon each renewal.
```

6. `sample_contracts/mutual_nda.txt`:
```
SECTION 1. CONFIDENTIAL INFORMATION
1.1 Protection. Each party agrees to hold the other's Confidential Information in strict confidence and not to disclose such information to any third party for a period of three (3) years from the date of disclosure.
```

================================================================================
20. VERIFICATION & AUTOMATED TEST SUITE (16/16 PYTEST SPECIFICATIONS)
================================================================================
The codebase must pass all 16 automated integration tests with zero errors:
1. `backend/tests/test_api_integration.py`:
   - Health check endpoint verification (`GET /health`).
   - Demo contract load & analysis execution (`POST /api/v1/contracts/demo/...`).
   - Contracts listing and detail verification (`GET /api/v1/contracts/` & `GET /api/v1/contracts/{id}`).
   - DOCX Track Changes export file verification (`GET /api/v1/analysis/{id}/export/docx`).
   - Audit telemetry summary verification (`GET /api/v1/analysis/audit/summary`).
2. `backend/tests/test_contractmind.py`:
   - PII redaction accuracy across SSN, email, phone, credit card, bank account, tax ID.
   - PyMuPDF text & Markdown table extraction.
   - Contextual RAG indexing & query retrieval.
   - Word Track Changes low-level XML `<w:ins>` and `<w:del>` verification with author attribution.
   - MCP tools registration and JSON-RPC execution.
3. `backend/tests/test_v152_features.py`:
   - Redline Accept / Reject PATCH persistence (`PATCH /api/v1/analysis/{id}/redlines/{rl_id}`).
   - AI prompt rewriting with diff token recomputation (`POST .../regenerate`).
   - Risk severity query filtering (`risk_severity=CRITICAL`).
   - Decision status query filtering (`decision=accepted`).
4. `backend/tests/test_v153_enhancements.py`:
   - SSE debate stream connectivity and history replay (`/api/v1/stream/{id}` & `/api/v1/stream/debate/{id}`).
   - iCalendar RFC 5545 (.ics) export formatting and VEVENT attributes (`/export/ics` & `/export/calendar`).
   - Full audit JSON and CSV matrix export downloads (`/export/json` & `/export/csv`).
   - Side-by-side contract comparison endpoint and risk delta calculation (`/api/v1/contracts/compare`).
   - Custom playbook CRUD operations (`GET`, `POST`, `DELETE /api/v1/playbook/custom`).
   - LLM health probe telemetry (`/api/v1/analysis/llm/health`).
   - User registration and bearer token authentication (`/api/v1/auth/register` & `/api/v1/auth/login`).
   - Contract deletion with disk file and vector cleanup (`DELETE /api/v1/contracts/{id}`).
```
