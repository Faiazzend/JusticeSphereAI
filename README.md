# 🏛️ ContractMind v1.5.3 — Autonomous Multi-Agent Legal AI Studio

> **Version:** 1.5.3  
> **Track:** JusticeSphere_AI — AI Builders Congress 2026  
> **Repository:** [https://github.com/Faiazzend/JusticeSphereAI](https://github.com/Faiazzend/JusticeSphereAI)

---

## 📖 Executive Summary

**ContractMind v1.5.3** is an enterprise-grade autonomous legal intelligence platform that ingests complex commercial agreements, conducts adversarial multi-agent debate, synthesizes consensus redlines into genuine Word (`.docx`) Track Changes format, and extracts structured compliance obligation matrices with instant calendar integration.

---

## 🚀 Key Architectural Innovations

### 1. Multi-Agent StateGraph Pipeline (4 Specialized Roles)
1. **Auditor Agent:** Enterprise compliance defender scanning across 10 critical risk categories (AI model training, first-dollar tipping indemnity baskets, warranty qualifiers, IP grant-backs, etc.).
2. **Opposing Counsel Agent:** Counterparty negotiator aggressively challenging unilateral compliance claims with commercial counterarguments and compromises.
3. **Redline Synthesizer Agent:** Impartial consensus arbiter synthesizing balanced compromise language and computing composite risk scores.
4. **Obligation Extractor Agent:** Compliance monitor extracting structured role matrices (obligor, recipient, triggers, recurrence, breach penalties).

### 2. Lawyer-in-the-Loop Decisions & AI Prompt Rewriter
- **Accept / Reject / Reset Action Toolbar:** Lawyers can individually accept or reject proposed clauses, which dynamically alters downstream Word (`.docx`) OpenXML export logic.
- **AI Prompt Rewriter Panel:** In-line rewriting allows legal teams to type natural language instructions or select quick-chips (`+ Make Mutual`, `+ 1x Annual Cap`, `+ 30-Day Cure`, `+ Strike AI Training`) to instantly re-synthesize redlines.
- **Decision-Branching DOCX Output:** Accepted clauses inject native `<w:ins>` and `<w:del>` OpenXML Track Changes markup; rejected clauses cleanly preserve original contract language.

### 3. Multi-Format Export Suite
- **Native Word Track Changes (`.docx`):** Produces genuine `<w:ins>` and `<w:del>` markup recognized by Microsoft Word's review ribbon.
- **iCalendar Compliance Calendar (`.ics`):** Exports all extracted covenants and operational deadlines formatted to RFC 5545 for 1-click import into Google Calendar, Microsoft Outlook, or Apple Calendar.
- **Structured JSON Analysis (`.json`):** Full machine-readable audit report for CLM integration (Ironclad, Agiloft, etc.).
- **Redlines & Obligations CSV (`.csv`):** Tabular CSV export of recommendations and obligation matrices.

### 4. Side-by-Side Contract Version Comparison & Risk Delta
- Instant visual diff comparison between two agreements (e.g. Master Agreement vs Counterparty Draft).
- Displays word-level diff tokens, added/removed/modified sections, and computed risk score variance delta.

### 5. Real-Time Live Streaming (SSE with Queue Pub/Sub)
- Low-latency Server-Sent Events (`/api/v1/stream/{id}`) with queue subscription, debate transcript replay, and automatic heartbeat keep-alive.

### 6. Contextual RAG & PII Sanitization
- Regex-based PII redaction strips SSNs, credit cards, bank accounts, and tax IDs before ingestion.
- PyMuPDF (`fitz`) parses text and converts complex embedded document tables into clean Markdown exhibits.
- Contextual semantic chunking with ChromaDB vector search and an automatic fallback to in-memory term-frequency cosine scoring.

### 7. Dual Inference Engine with LLM Provider Health Diagnostics
- Supports **Google Gemini 2.0 Flash**, Local **Ollama** (`qwen3.5:4b`), OpenAI GPT-4o, and Anthropic Claude.
- Real-time diagnostic health check endpoint (`/api/v1/analysis/llm/health`) reporting latency and connectivity.
- High-caliber deterministic legal fallback core ensures 100% SLA even during network outages.

### 8. Model Context Protocol (MCP) Gateway
- Exposes standardized JSON-RPC tools (`evaluate_clause`, `get_playbook_rules`, `calculate_risk_matrix`) at `/mcp/tools` and `/mcp/call`.

### 9. Alpine.js Neo-Legal Studio with 7-Step Guided Tour
- Zero React build required for standalone studio. Features a 7-step interactive tour with high-intensity glowing halo spotlights (`box-shadow: 0 0 0 11px rgba(91, 103, 246, 0.8)`).

---

## 🛠️ Quickstart

### Option A: 1-Click Launch (Windows)
Double-click:
```cmd
run_contractmind.bat
```

### Option B: Python CLI Launch
```bash
# 1. Install dependencies
pip install -r backend/requirements.txt

# 2. Launch orchestrator
python launch.py
```
Server starts on `http://localhost:8000` and automatically opens your default browser.

---

## 🌐 API Endpoints

- `GET /` & `GET /studio`: Serves the Alpine.js Neo-Legal Studio.
- `POST /api/v1/contracts/upload`: PDF/TXT ingestion with PyMuPDF table parsing and PII redaction.
- `POST /api/v1/contracts/demo/{sample_type}`: 1-Click auto-analysis of benchmark contracts (`ma`, `cloud_dpa`, `joint_ip`, `msa`, `saas`, `nda`).
- `GET /api/v1/contracts/`: List all analyzed agreements (with `skip` & `limit` pagination).
- `GET /api/v1/contracts/{id}`: Detailed contract report.
- `DELETE /api/v1/contracts/{id}`: Purge contract, delete disk file, and clear ChromaDB collection.
- `POST /api/v1/contracts/compare`: Side-by-side contract comparison and risk delta.
- `POST /api/v1/analysis/{id}/trigger`: Trigger 4-agent stategraph analysis.
- `GET /api/v1/analysis/{id}/redlines`: Filter redlines by `risk_severity` and `decision` status.
- `PATCH /api/v1/analysis/{id}/redlines/{redline_id}`: Update lawyer decision (`accepted: true/false/null`).
- `POST /api/v1/analysis/{id}/redlines/{redline_id}/regenerate`: Lawyer AI prompt rewriter.
- `GET /api/v1/analysis/{id}/export/docx`: Native Word Track Changes document.
- `GET /api/v1/analysis/{id}/export/ics`: RFC 5545 iCalendar compliance schedule.
- `GET /api/v1/analysis/{id}/export/json`: Complete analysis export in structured JSON.
- `GET /api/v1/analysis/{id}/export/csv`: Tabular CSV of redlines and obligations.
- `GET /api/v1/analysis/stream/{id}`: Real-time SSE debate stream.
- `GET /api/v1/analysis/llm/health`: Provider latency and diagnostic status.
- `GET /api/v1/analysis/audit/summary`: Real-time token and USD cost telemetry.
- `GET /api/v1/playbook/`: List institutional negotiation playbooks.
- `POST /api/v1/playbook/custom`: Create custom negotiation playbook.
- `GET /mcp/tools` & `POST /mcp/call`: Model Context Protocol tools gateway.
- `GET /health`: System health status (`{"status": "healthy", "version": "1.5.3"}`).

---

## 🧪 Automated Test Suite

Run the full pytest suite (15 unit and integration tests):
```bash
python -m pytest backend/tests -v
```

---

## 🚢 Production Deployment (Vercel Multi-Service)
Configured via `vercel.json` with multi-service bindings:
- Backend: FastAPI service routed to `/api/*`, `/health`, `/mcp/*`
- Frontend: Next.js bridge route handler serving the studio with server-side rewrites.

---

## 📜 License
Licensed under Apache 2.0. Built for the **AI Builders Congress 2026** (Track: *JusticeSphere_AI*).
