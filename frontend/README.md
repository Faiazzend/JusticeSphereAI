# ContractMind Frontend

Modern AI-Native Contract Intelligence UI built with Next.js 14+ (App Router), TypeScript, and Tailwind CSS for the **AI Builders Congress 2026 Hackathon**.

## 🌟 Core Features & Views
1. **Interactive Redline Studio (`/contracts/[id]`):**
   - Track Changes view with color-coded strike-through and underline markup.
   - Side-by-side split view comparing original clauses vs. AI consensus counter-proposals.
   - Clause Action Bar: Accept Redline, Reject, or Reset.
   - Popover revealing agent legal rationale, severity ratings, and citations.
2. **Live Multi-Agent Debate Feed:**
   - Real-time Server-Sent Events (SSE) stream of the debate between **Auditor Agent** (Defender) and **Opposing Counsel Agent**.
3. **Executive Risk Scorecard (`/contracts/[id]/risks`):**
   - Animated SVG circular gauge computing composite risk score (0-100).
   - Categorized risk cards breaking down indemnifications, liability caps, and termination rights.
4. **Structured Obligations Matrix & Calendar (`/contracts/[id]/obligations`):**
   - Filterable data table categorizing payments, insurance requirements, delivery milestones, and penalties.
   - One-click export to standard **iCalendar (.ICS)** for Google Calendar / Apple Calendar sync.
5. **Observability & Audit Dashboard (`/audit`):**
   - Displays real-time token consumption, estimated USD cloud costs, average agent latency, and PII anonymization status for hackathon judges.

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment
Copy `.env.local.example` to `.env.local`:
```bash
cp .env.local.example .env.local
```

### 3. Run Development Server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.
Ensure your ContractMind backend server is running on `http://localhost:8000`.
