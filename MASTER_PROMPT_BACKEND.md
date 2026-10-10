You are a Principal AI & Backend Systems Architect. You are building the complete, production-grade backend for "ContractMind"—an AI-native contract intelligence platform that automates PDF contract ingestion, playbook-driven risk scoring, multi-agent redlining, and structured obligations extraction.

STRICT CODE QUALITY MANDATE:
- Do NOT output placeholders, ellipses (...), or "// TODO: implement later". Every function, schema, route, and agent node must be fully implemented with production-grade logic.
- Implement strict typing with Python 3.11+, Pydantic v2, and robust error handling.
- Concurrency and streaming must be natively supported using FastAPI and asynchronous I/O.

================================================================================
1. TECHNOLOGY STACK & ARCHITECTURE
================================================================================
- Language & Runtime: Python 3.11+
- Web Framework: FastAPI with Uvicorn (async/await throughout)
- Agent Orchestration: LangGraph (StateGraph with checkpointing & cyclic debate)
- LLM Gateway: LiteLLM or LangChain supporting multi-provider fallback (Primary: Anthropic Claude 3.5 Sonnet / OpenAI GPT-4o; Secondary/Local: Ollama with deepseek-r1 / qwen2.5)
- Multimodal & PDF Engine: PyMuPDF (fitz), pdf2image, pytesseract/pdfplumber for hybrid extraction, vision-based table parser for complex exhibits
- Embeddings & Vector Store: ChromaDB or Qdrant with Contextual RAG (chunk prepending) and Semantic Chunking
- Model Context Protocol (MCP): Built-in MCP Server using the official `mcp` Python SDK exposing contract evaluation tools via Stdio and SSE
- Audit & Security: Token usage counter, PII redactor (regex/presidio-lite), JWT-based RBAC (Admin, Legal Reviewer), SQLite/PostgreSQL persistence via SQLAlchemy async

================================================================================
2. DIRECTORY STRUCTURE TO GENERATE
================================================================================
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI entrypoint with CORS, middlewares, lifespan
│   ├── config.py                   # Pydantic BaseSettings (API keys, Ollama host, DB URLs)
│   ├── database.py                 # Async SQLAlchemy engine & session factory
│   ├── models/                     # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── contract.py             # Contract metadata, raw_text, status, file_path
│   │   ├── audit.py                # Token usage, latency, agent step logs, user audits
│   │   └── user.py                 # RBAC users (Admin, Reviewer) & API keys
│   ├── schemas/                    # Pydantic v2 request/response models
│   │   ├── __init__.py
│   │   ├── contract_schemas.py     # Upload response, contract status, redline diff schema
│   │   ├── obligation_schemas.py   # Structured Obligations JSON (Deadlines, Penalties, Parties)
│   │   ├── risk_schemas.py         # Risk scores (0-100), clause categories, risk severity
│   │   └── playbook_schemas.py     # Custom playbook rules (Gold Standard benchmarks)
│   ├── core/                       # Security, auth, sanitization
│   │   ├── __init__.py
│   │   ├── security.py             # JWT generation, hash verification, role guards
│   │   ├── pii_redactor.py         # Anonymizes SSN, bank accounts, emails before LLM call
│   │   └── token_tracker.py        # Token counting & cost tracking per agent invocation
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pdf_processor.py        # Hybrid PDF parser: text extraction + vision table capture
│   │   ├── rag_engine.py           # Contextual RAG, Semantic chunking, Vector store retriever
│   │   ├── diff_engine.py          # Unified diff generation & structured redline builder
│   │   └── export_service.py       # Generates DOCX with Track Changes and marked PDF
│   ├── agents/                     # LangGraph Multi-Agent Architecture
│   │   ├── __init__.py
│   │   ├── state.py                # ContractReviewState definition
│   │   ├── nodes/
│   │   │   ├── auditor_agent.py    # Agent A: Flags non-compliance against Playbook
│   │   │   ├── opposing_agent.py   # Agent B: Represents counterparty, proposes compromises
│   │   │   ├── redline_agent.py    # Agent C: Generates surgical redlines & reasoning
│   │   │   └── obligation_agent.py # Agent D: Extracts calendar obligations & penalty JSON
│   │   └── graph.py                # StateGraph orchestration, conditional edges, supervisor
│   ├── mcp_server/                 # Custom MCP Server (Model Context Protocol)
│   │   ├── __init__.py
│   │   └── server.py               # Exposes tools: evaluate_clause, get_playbook, search_precedents
│   └── api/                        # REST & Streaming endpoints
│       ├── __init__.py
│       ├── deps.py                 # Dependency injections (DB session, current user)
│       ├── v1/
│       │   ├── auth.py             # Login, register, token refresh
│       │   ├── contracts.py        # Upload PDF, get status, list contracts
│       │   ├── analysis.py         # Trigger analysis, get risks, obligations, redlines
│       │   ├── stream.py           # SSE endpoint streaming multi-agent debate logs in real-time
│       │   └── playbook.py         # CRUD custom playbooks (e.g., Aggressive Startup vs Enterprise)
├── tests/
│   ├── test_pdf_processing.py
│   ├── test_agents.py
│   └── test_rag.py
├── requirements.txt
├── Dockerfile
└── README.md

================================================================================
3. CORE SYSTEM IMPLEMENTATION SPECIFICATIONS
================================================================================

A. MULTI-AGENT STATEGRAPH (app/agents/):
Define a comprehensive `ContractReviewState` TypedDict containing:
- `raw_text`: str
- `sections`: List[Dict[str, Any]]
- `playbook_rules`: List[Dict[str, Any]]
- `identified_risks`: List[RiskItem] (Clause, Severity: HIGH/MED/LOW, Score, Rationale)
- `debate_turns`: List[DebateMessage] (Agent name, proposed clause, counter-proposal, debate transcript)
- `redlines`: List[RedlineChange] (Original, Suggested, DiffType: INSERT/DELETE/REPLACE, LegalRationale)
- `obligations`: List[ObligationItem] (Party, Obligation, Deadline/Trigger, Penalty, Frequency)
- `overall_score`: float (0 to 100)

Implement the cyclic debate workflow:
1. `AuditorAgent`: Analyzes clauses against Playbook rules (e.g., Indemnification uncapped = Critical Risk).
2. `OpposingAgent`: Simulates aggressive counterparty arguments, identifying commercially viable compromises.
3. `SupervisorNode`: Determines if consensus is reached or loops back (max 2 debate cycles).
4. `RedlineAgent`: Produces precision redlines with rationale.
5. `ObligationAgent`: Extracts milestone deliverables, financial obligations, and termination windows into strict JSON.

B. CONTEXTUAL RAG & SEMANTIC CHUNKING (app/services/rag_engine.py):
- Implement Semantic Chunking: Split contract documents on clause/section boundaries rather than rigid character counts.
- Implement Contextual RAG: For each chunk, invoke an LLM to generate a concise 1-sentence contextual preface (e.g., "In Section 12 (Indemnification) of the Acme MSA regarding IP infringement...") and prepend it to the text chunk before embedding.
- Store chunks and embeddings with metadata (section_number, page_number, clause_type).
- Support fallback retrieval: Exact keyword search (BM25) combined with dense vector similarity (Hybrid Search).

C. MULTIMODAL & PDF PARSER (app/services/pdf_processor.py):
- Ingest raw PDF byte stream.
- Extract native text with bounding coordinates.
- Detect tables: Render table pages into high-res images and pass to Vision LLM prompt to convert complex financial/milestone matrices into Markdown tables and JSON calendars without OCR corruption.
- Clean and normalize text, flagging exhibits and appendices.

D. STRUCTURED JSON OBLIGATIONS SCHEMA (app/schemas/obligation_schemas.py):
The obligations endpoint must strictly return:
```json
{
  "contract_id": "uuid",
  "summary": "Executive summary of contract obligations",
  "overall_risk_score": 78.5,
  "obligations": [
    {
      "id": "obl_001",
      "clause_reference": "Section 8.2",
      "obligor": "Vendor",
      "recipient": "Client",
      "obligation_type": "Payment | Insurance | Delivery | Audit | Termination",
      "description": "Provide certificate of cybersecurity insurance within 30 days of execution.",
      "due_date_or_trigger": "30 days post-execution",
      "recurrence": "Annual",
      "penalty_for_breach": "Immediate right to terminate for cause without cure period",
      "is_critical": true
    }
  ]
}
```

E. CUSTOM MCP SERVER (app/mcp_server/server.py):
- Implement an MCP server using `mcp.server.fastmcp.FastMCP`.
- Expose 3 functional tools:
  1. `evaluate_clause(clause_text: str, playbook_type: str)`: Returns compliance verdict and legal citations.
  2. `get_playbook_rules(playbook_id: str)`: Retrieves the standard clauses for liability caps, governing law, and indemnification.
  3. `calculate_risk_matrix(obligations: list, liabilities: list)`: Computes composite risk score.
- Support both SSE transport (`/mcp/sse`) and Stdio transport for external host agent integration.

F. TOKEN AUDIT & OBSERVABILITY (app/core/token_tracker.py):
- Intercept every LLM call.
- Log prompt tokens, completion tokens, latency (ms), model used, and calculated USD cost into the SQLite/PostgreSQL `audit_logs` table.
- Provide a GET `/api/v1/analysis/audit-summary` endpoint for hackathon judge compliance verification.

================================================================================
4. DELIVERABLE INSTRUCTIONS
================================================================================
Generate the full, runnable backend codebase starting from `requirements.txt`, `config.py`, database models, services, LangGraph multi-agent nodes, MCP server, and FastAPI routers. Ensure all imports are accurate and all endpoints are tested and ready to connect to the frontend.
