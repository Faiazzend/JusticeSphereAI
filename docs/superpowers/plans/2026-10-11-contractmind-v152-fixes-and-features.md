# ContractMind v1.5.2 Bug Fixes, High-Value Features & GitHub Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve all 4 critical bugs and 14 high/medium issues identified in the codebase audit, implement high-value legal features (real-time live SSE broadcasting, iCalendar .ics export, JSON/CSV exports, contract version comparison, custom playbooks, and LLM health checks), update the Alpine.js studio, and deploy to GitHub at `https://github.com/Faiazzend/JusticeSphereAI`.

**Architecture:** Enhances FastAPI backend endpoints with real-time SSE pub/sub event broadcasting, non-blocking asynchronous file operations, strict input validation, resilient node-level exception isolation in the LangGraph-style agent graph, and RFC-standard document exports (.ics, CSV, JSON, DOCX). Updates Alpine.js Neo-Legal Studio frontend with reactive controls and synchronizes Next.js routes.

**Tech Stack:** Python 3.12+, FastAPI, SQLAlchemy (Async SQLite), Pydantic v2, ChromaDB / TF-IDF, PyMuPDF, python-docx, Alpine.js 3.14+, Tailwind CSS, Git / GitHub CLI.

**Spec:** `C:\Users\pc\.gemini\antigravity\brain\293905a1-316b-4090-b22c-aa9bc66cfedf\improvement_report.md` and `MASTER_PROMPT.md`

## Global Constraints

- Preserve all existing tests and ensure all pass (`pytest backend/tests`).
- Maintain backward compatibility for all existing API schemas and frontend components.
- Do not introduce breaking dependencies for existing users; use stdlib where feasible (e.g. `csv`, RFC 5545 iCalendar generation).
- All new async endpoints must not block the uvicorn event loop (`asyncio.to_thread` for CPU/disk-bound tasks).
- Model reference defaults should be `gemini-2.0-flash`.

## Review Focus

1. **Live SSE Disconnections:** Client disconnects during streaming must cleanly stop the generator without leaking memory or throwing unhandled CancelledErrors.
2. **Calendar Timezone Formatting:** Obligation `.ics` exports must output compliant UTC `DTSTART` and `UID` formats accepted by Google Calendar and Microsoft Outlook.
3. **Upload Security & Atomicity:** Uploading invalid or oversized files must fail early with proper HTTP status codes, and database errors must immediately unlink temporary files.
4. **Agent Graph Partial Failures:** If an LLM node encounters a network timeout, the pipeline must log the error, record a fallback turn in the debate transcript, and complete the analysis without setting the contract status to fatal crash.
5. **Git Synchronization:** Merging with existing GitHub remote `Faiazzend/JusticeSphereAI` must preserve git history and commit cleanly to `main`.

---

### Task 1: Core Bug Fixes & Infrastructure Cleanup

**Files:**
- Modify: `backend/requirements.txt`
- Modify: `backend/app/agents/llm_client.py`
- Modify: `backend/app/api/v1/contracts.py`
- Modify: `backend/app/api/v1/analysis.py`
- Create: `backend/tests/__init__.py`

**Interfaces:**
- Consumes: `settings`, `ContractDetailResponse`
- Produces: Sanitized upload validation, file deletion on contract removal, pagination parameters, updated model defaults (`gemini-2.0-flash`).

- [ ] **Step 1: Update dependencies in `backend/requirements.txt`**
Add `chromadb>=0.4.24` and ensure all required packages are present.

- [ ] **Step 2: Fix phantom model name and timeout in `backend/app/agents/llm_client.py`**
Change default model from `gemini-3.5-flash-lite` to `gemini-2.0-flash`. Update `timeout = httpx.Timeout(60.0, connect=5.0, read=60.0)` and increase `maxOutputTokens` to 4096.

- [ ] **Step 3: Update model name references in `backend/app/api/v1/analysis.py` and `backend/app/api/v1/contracts.py`**
Replace hardcoded `gemini-3.5-flash-lite` with `gemini-2.0-flash`.

- [ ] **Step 4: Add file validation and atomic cleanup in `backend/app/api/v1/contracts.py`**
Add size check (max 25MB) and content type check. Clean up file on disk if DB commit fails. Delete file on disk in `delete_contract`. Add `skip: int = 0, limit: int = 50` pagination to `list_contracts`.

- [ ] **Step 5: Create `backend/tests/__init__.py`**
Touch empty `__init__.py`.

- [ ] **Step 6: Run existing tests to verify baseline**
Run: `pytest backend/tests -v`
Expected: 10 passed.

---

### Task 2: Resilient Agent Graph & RAG Optimization

**Files:**
- Modify: `backend/app/services/rag_engine.py`
- Modify: `backend/app/agents/graph.py`
- Modify: `backend/app/api/v1/analysis.py`

**Interfaces:**
- Consumes: `ContractReviewState`, `auditor_node`, `opposing_node`, `redline_node`, `obligation_node`
- Produces: Per-node failure isolation, live event streaming queue hook, non-blocking DOCX export.

- [ ] **Step 1: Improve RAG engine robustness in `backend/app/services/rag_engine.py`**
Gracefully catch ChromaDB initialization/embedding issues and fall back seamlessly to token frequency similarity scoring.

- [ ] **Step 2: Refactor `backend/app/agents/graph.py` for per-node resilience and event broadcasting**
Add `broadcast_event(contract_id, event_data)` mechanism and wrap each node (`auditor_node`, `opposing_node`, `redline_node`, `obligation_node`) in isolated try-except blocks so a single agent hiccup does not abort the entire review.

- [ ] **Step 3: Make DOCX export non-blocking in `backend/app/api/v1/analysis.py`**
Run `export_service.generate_docx_redline` via `asyncio.to_thread`. Add `response_model=List[RedlineItem]` to `GET /api/v1/analysis/{id}/redlines`.

- [ ] **Step 4: Verify test suite**
Run: `pytest backend/tests -v`
Expected: 10 passed.

---

### Task 3: Real-Time SSE Broadcasting & LLM Health Diagnostics

**Files:**
- Modify: `backend/app/api/v1/stream.py`
- Modify: `backend/app/api/v1/analysis.py`
- Modify: `backend/app/schemas/contract_schemas.py`

**Interfaces:**
- Consumes: `broadcast_event` from `graph.py`
- Produces: `GET /api/v1/stream/{id}` live event stream, `GET /api/v1/analysis/llm/health` diagnostics.

- [ ] **Step 1: Implement real-time SSE stream with queue pub/sub in `backend/app/api/v1/stream.py`**
Subscribe to live events emitted during graph execution. Support backlog replay of `debate_transcript` and real-time yield with proper headers (`Cache-Control: no-cache`, `X-Accel-Buffering: no`, `Connection: keep-alive`).

- [ ] **Step 2: Add LLM Provider Health Check endpoint in `backend/app/api/v1/analysis.py`**
Implement `GET /api/v1/analysis/llm/health` returning latency and status for configured providers (Gemini, OpenAI, Anthropic, Ollama, Fallback).

- [ ] **Step 3: Write tests for stream headers and LLM health endpoint**
Create test cases in a new test file `backend/tests/test_v153_enhancements.py`.

- [ ] **Step 4: Run tests**
Run: `pytest backend/tests -v`
Expected: PASS.

---

### Task 4: New Productivity & Export Features (Calendar .ics, CSV/JSON, Delta Compare, Custom Playbooks)

**Files:**
- Modify: `backend/app/api/v1/analysis.py`
- Modify: `backend/app/api/v1/contracts.py`
- Modify: `backend/app/api/v1/playbook.py`
- Modify: `backend/app/schemas/playbook_schemas.py`

**Interfaces:**
- Consumes: Contract obligations, `diff_engine`
- Produces:
  - `GET /api/v1/analysis/{id}/export/ics` (RFC 5545 iCalendar)
  - `GET /api/v1/analysis/{id}/export/json` (Structured JSON)
  - `GET /api/v1/analysis/{id}/export/csv` (Redlines & Obligations CSV)
  - `POST /api/v1/contracts/compare` (Version comparison diff)
  - `POST /api/v1/playbook/custom` & `GET /api/v1/playbook/custom`

- [ ] **Step 1: Implement iCalendar (.ics) export in `backend/app/api/v1/analysis.py`**
Generate RFC 5545 compliant `.ics` calendar file with VEVENT items for all extracted obligations with due dates / triggers.

- [ ] **Step 2: Implement JSON and CSV export endpoints in `backend/app/api/v1/analysis.py`**
Implement `GET /api/v1/analysis/{id}/export/json` and `GET /api/v1/analysis/{id}/export/csv` returning downloadable files.

- [ ] **Step 3: Implement Contract Comparison endpoint in `backend/app/api/v1/contracts.py`**
Accept two contract IDs (or contract texts) and return side-by-side section diffs with additions, deletions, and risk delta.

- [ ] **Step 4: Implement Custom Playbook management in `backend/app/api/v1/playbook.py`**
Support creating and retrieving custom user playbooks stored in SQLite or memory.

- [ ] **Step 5: Write unit and integration tests for all 4 new features**
Add tests in `backend/tests/test_v153_enhancements.py`.

- [ ] **Step 6: Run full test suite**
Run: `pytest backend/tests -v`
Expected: All tests pass.

---

### Task 5: Frontend Studio Enhancements & Reactivity

**Files:**
- Modify: `backend/static/index.html`
- Modify: `frontend/public/index.html`

**Interfaces:**
- Consumes: New API endpoints (.ics, JSON, CSV, LLM health, compare, updated model defaults)
- Produces: Updated interactive UI with iCalendar download, JSON/CSV exports, LLM Health dialog, comparison trigger, and reactive Alpine.js state.

- [ ] **Step 1: Fix Alpine.js reactivity for rewrite prompts**
Initialize `this.rewritePrompts = {}` and ensure deep reactivity when loading redlines.

- [ ] **Step 2: Add Export Modal options (.ics Calendar, JSON, CSV) and LLM Health Check indicator**
Add buttons in UI to download iCalendar (.ics), JSON, and CSV exports. Add an LLM provider status pill.

- [ ] **Step 3: Update model selector default to `gemini-2.0-flash`**
Ensure dropdown and trigger defaults use modern Gemini 2.0 Flash.

- [ ] **Step 4: Sync `frontend/public/index.html` with `backend/static/index.html`**
Ensure both frontend entry points are identical.

- [ ] **Step 5: Verify frontend build**
Run: `cd frontend && npm run build`
Expected: Build succeeds with 0 errors.

---

### Task 6: Git Setup, Commit & Push to GitHub Repo

**Files:**
- Repository root: `c:\Users\pc\Desktop\mockup`

**Interfaces:**
- GitHub remote: `https://github.com/Faiazzend/JusticeSphereAI.git`
- Branch: `main`

- [ ] **Step 1: Initialize Git repo and configure remote**
Run `git init`, set branch `main`, add remote `origin https://github.com/Faiazzend/JusticeSphereAI.git`.

- [ ] **Step 2: Fetch and align with remote branch**
Handle any unmerged files or divergence cleanly so remote history is preserved.

- [ ] **Step 3: Commit all updated files with clean conventional commit message**
Stage files (excluding temporary caches, .venv, node_modules, .db files), commit: `feat: ContractMind v1.5.3 — live SSE, iCalendar export, JSON/CSV export, resilient agent graph, bug fixes`.

- [ ] **Step 4: Push to GitHub `origin main`**
Run `git push origin main` using user credentials.

- [ ] **Step 5: Verify GitHub repo state**
Check `gh repo view` to ensure the repository has the latest code.
