# ContractMind Backend

AI-Native Contract Intelligence, Multi-Agent Redlining & Obligation Extraction Engine built for the **AI Builders Congress 2026 Hackathon**.

## 🚀 Key Architectural Features
1. **Multi-Agent StateGraph Loop:**
   - **Auditor Agent:** Discovers high-risk deviations against standard playbooks (e.g., uncapped indemnities).
   - **Opposing Counsel Agent:** Counter-argues from the counterparty's standpoint and offers market compromises.
   - **Redline Synthesizer:** Reconciles the debate, generating surgical text replacements with word-level diff tokens.
   - **Obligation Extractor:** Outputs typed JSON of calendar deadlines, payment triggers, and breach penalties.
2. **Contextual RAG & Semantic Chunking:**
   - Prepends chunk-specific document hierarchy context prior to vector embeddings in ChromaDB.
3. **Multimodal & PDF Ingestion:**
   - PyMuPDF integration with native table structure and exhibit parsing.
4. **Custom Model Context Protocol (MCP) Server:**
   - Exposes `evaluate_clause`, `get_playbook_rules`, and `calculate_risk_matrix` tools via HTTP/SSE and Stdio.
5. **Observability & Guardrails:**
   - PII redactor (anonymizing SSN, banking, and emails).
   - Token & cost tracking with live audit logging table for judge inspection.

---

## 🛠️ Quick Start

### 1. Install Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Environment Variables (.env)
Create a `.env` file in `backend/`:
```env
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=gpt-4o
FALLBACK_MODEL=deepseek-r1:latest
SECRET_KEY=contractmind_secret_jwt_key
```

### 3. Run the Backend Server
```bash
python -m app.main
```
Or via Uvicorn:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- MCP Tools Registry: [http://localhost:8000/mcp/tools](http://localhost:8000/mcp/tools)

---

## 🧪 Running Tests
```bash
pytest
```
