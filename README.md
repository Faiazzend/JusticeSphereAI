# ⚖️ ContractMind v1.5 — Autonomous Multi-Agent Legal AI Studio

> **AI Builders Congress 2026 — Track: JusticeSphere_AI**  
> *AI-Native Contract Intelligence, Multi-Agent Redlining Debate, & Obligation Extraction Engine*

---

## 🌟 Overview

**ContractMind v1.5** is an enterprise-grade autonomous legal AI studio designed to automate contract review, commercial negotiation, and compliance audits. Powered by a **Cyclic Multi-Agent StateGraph**, it orchestrates an adversarial legal debate between specialized AI personas to produce consensus redlines, structured obligation matrices, and native Microsoft Word Track Changes documents in under 2 seconds.

---

## 🏛️ Core Architecture: Cyclic Multi-Agent Debate

```
   ┌────────────────────────────────────────────────────────┐
   │                   Raw Agreement PDF                    │
   └───────────────────────────┬────────────────────────────┘
                               │
                  [PyMuPDF + PII Redaction]
                               ▼
            [Contextual RAG Semantic Chunking Engine]
                               │
    ┌──────────────────────────┴──────────────────────────┐
    │                                                     │
    ▼                                                     ▼
┌────────────────────────┐              ┌────────────────────────┐
│    Auditor Agent       │  ◄────────►  │ Opposing Counsel Agent │
│ (Internal Enterprise)  │              │ (Counterparty Advocate)│
└───────────┬────────────┘              └───────────┬────────────┘
            │                                       │
            └───────────────────┬───────────────────┘
                                ▼
                 ┌─────────────────────────────┐
                 │  Redline Synthesizer Agent  │
                 │   (Consensus & Compromise)  │
                 └──────────────┬──────────────┘
                                │
                                ▼
                 ┌─────────────────────────────┐
                 │  Obligation Extractor Agent │
                 │ (Milestones, Dates & Fines) │
                 └──────────────┬──────────────┘
                                │
                                ▼
       ┌────────────────────────────────────────────────┐
       │ - Real-Time Diff Viewer (Insert/Delete/Equal)  │
       │ - Word Track Changes (.docx) OpenXML Export    │
       │ - Structured Obligations Table Matrix          │
       │ - Model Context Protocol (MCP) Tools Gateway   │
       └────────────────────────────────────────────────┘
```

1. **Auditor Agent (Enterprise Defender):** Analyzes contract clauses against chosen negotiation playbooks, identifying uncapped indemnification, AI training traps, and liability exposure.
2. **Opposing Counsel Agent (Counterparty Advocate):** Pushes back on overly restrictive terms, offering commercially viable compromises to preserve deal velocity.
3. **Redline Synthesizer Agent (Consensus Arbiter):** Reconciles the debate, formulating balanced redline replacements with word-level diff tokens and legal rationales.
4. **Obligation Extractor Agent:** Extracts operational duties, obligor/recipient roles, calendar triggers, and breach penalties into structured tabular data.

---

## 🚀 Key Features

* **Dual Inference Engine:** 
  * Cloud: **Google Gemini 3.5 Flash Lite** (sub-2s latency, ~$0.000075/1K tokens).
  * Local Privacy Core: **Local Ollama** (`qwen3.5:4b`), running completely offline with automatic cloud failover.
* **OpenXML Native Track Changes:** Generates authentic `.docx` files with native `<w:ins>` and `<w:del>` markup compatible with Microsoft Word's "Accept/Reject All Changes" review ribbon.
* **PII Redaction Pipeline:** Automatic regex sanitization of SSNs, credit cards, bank accounts, and tax IDs prior to embedding or LLM transmission.
* **Interactive Guided Webpage Rundown:** Step-by-step auto-advancing tour with high-intensity glowing spotlight halo (`#5B67F6`) and backdrop dimming.
* **Pre-Loaded Benchmark Evaluation Datasets:** 6 instant corporate deal benchmarks (Tech M&A, Cloud AI DPA, Joint IP R&D, Enterprise MSA, SaaS Agreement, Mutual NDA).
* **MCP FastServer Gateway:** Exposes standard Model Context Protocol endpoints at `/mcp/tools` and `/mcp/call`.
* **Execution Telemetry & Cost Audit:** Live token consumption, measured execution latency, and cost audit trail with reset functionality.

---

## ⚡ Quick Start

### 1. Requirements
* **Python 3.10+** (tested on Python 3.12, 3.14)
* **Git**
* (Optional) **Ollama** running locally on port `11434` with `qwen3.5:4b`

### 2. Setup & Installation
```bash
# Clone the repository
git clone https://github.com/Faiazzend/JusticeSphereAI.git
cd JusticeSphereAI

# Copy environment configuration
cp backend/.env.example backend/.env
```
Edit `backend/.env` to insert your `GEMINI_API_KEY` (or configure via the UI Settings modal).

### 3. Launching ContractMind
#### Windows (1-Click Launcher):
Simply double-click:
```bat
run_contractmind.bat
```

#### Terminal / Cross-Platform:
```bash
python launch.py
```
This automatically initializes the database, verifies dependencies, starts the FastAPI backend, and opens the Alpine.js Studio in your default browser at:
👉 **`http://localhost:8000`**

---

## 🧪 Testing

Run the automated test suite using pytest:
```bash
cd backend
python -m pytest -v tests
```

To run a live Gemini pipeline simulation:
```bash
cd backend
python test_gemini_nodes.py
```

---

## 📁 Repository Structure

```
JusticeSphere_AI/
├── backend/
│   ├── app/
│   │   ├── agents/          # LangGraph Multi-Agent StateGraph nodes & LLM gateway
│   │   ├── api/v1/          # FastAPI REST endpoints (analysis, contracts, telemetry)
│   │   ├── core/            # PII redactor, security, token tracker
│   │   ├── mcp_server/      # FastContract Model Context Protocol server
│   │   ├── models/          # SQLAlchemy async models (Contract, AuditLog, User)
│   │   ├── schemas/         # Pydantic v2 schemas
│   │   └── services/        # PDF extraction, Diff engine, RAG ChromaDB, DOCX export
│   ├── static/              # Alpine.js reactive UI frontend (index.html)
│   └── tests/               # Pytest async test suite
├── benchmarks/              # Comprehensive benchmark evaluation reports & ground truth
├── sample_contracts/        # 6 pre-loaded benchmark contract PDFs & text files
├── launch.py                # Process orchestrator & redirect server
├── run_contractmind.bat     # 1-click Windows execution batch file
└── README.md
```

---

## ⚖️ License
Developed for **AI Builders Congress 2026**. Distributed under the MIT License.
