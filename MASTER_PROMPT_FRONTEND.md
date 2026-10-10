You are a Principal Frontend Engineer and UI/UX Designer specializing in enterprise legal-tech applications. You are building the complete, responsive, production-ready frontend for "ContractMind"—an AI-native contract intelligence platform.

STRICT CODE QUALITY MANDATE:
- Do NOT output placeholder components, mock skeletons with missing functionality, or "// TODO" blocks.
- Build clean, accessible, modern UI using TypeScript, Next.js 14+ (App Router), Tailwind CSS, shadcn/ui components, and Lucide React icons.
- All views must feature high-polish micro-interactions, dark/light theme support, and seamless integration with the backend REST and SSE streaming endpoints.

================================================================================
1. CORE PAGES & USER WORKFLOWS TO BUILD
================================================================================
1. Global Layout & Header:
   - Modern glassmorphism header with ContractMind logo, Playbook Selector badge, Token & Cost live pill, and Dark/Light toggle.
   - Global status banner showing Multi-Agent connectivity and active MCP server link.

2. Document Ingestion Hub (/upload or /):
   - Drag-and-drop PDF dropzone supporting files up to 25MB.
   - Instant PDF client-side preview with thumbnail pages.
   - Playbook Configuration Drawer: Switch between "Aggressive Startup", "Enterprise Standard", and "Vendor Friendly" rules before analysis starts.
   - "Analyze Contract" CTA button with animated scanning states.

3. Interactive Redline Studio (/contracts/[id]):
   - Side-by-side or unified Track Changes View (Word/Google Docs style):
     * Red strike-through for deleted clauses.
     * Green highlight with underline for inserted clauses.
     * Hovering over any redline reveals the "Legal Rationale Tooltip" and agent citation.
   - Clause Action Bar: "Accept Change", "Reject Change", or "Custom Prompt Counter-offer".
   - Export Toolbar: "Export Redlined DOCX (Track Changes)", "Export Signed PDF", "Download JSON Schema".

4. Live Multi-Agent Debate Drawer / Feed:
   - Real-time collapsible terminal/feed connected to backend Server-Sent Events (SSE).
   - Visualizing Agent Dialogue:
     * 🛡️ Auditor Agent (Navy Blue): "Identified Section 9.1 Indemnity exceeds 2x contract value."
     * ⚖️ Opposing Counsel Agent (Orange/Amber): "Counter-proposing mutual indemnification capped at $500,000."
     * ✍️ Redline Synthesizer (Emerald Green): "Drafting consensus clause compliant with Playbook v2."
   - Visual turn counters and reasoning confidence badges.

5. Executive Risk Scorecard & Matrix (/contracts/[id]/risks):
   - Circular SVG gauge showing Overall Risk Score (0 to 100) with color dynamics (0-30 Green, 31-70 Amber, 71-100 Critical Red).
   - Categorized Risk Breakdown:
     * Limitation of Liability (Score & Severity)
     * IP Ownership & Licensing
     * Termination & Liquidated Damages
     * Non-Compete & Exclusivity
     * Data Privacy & Compliance (GDPR/CCPA badges)
   - Filterable risk cards with direct links that scroll to the corresponding clause in the Redline Studio.

6. Structured Obligations Matrix & Calendar (/contracts/[id]/obligations):
   - Interactive data table powered by TanStack Table:
     * Columns: Obligation Description, Obligor (Party), Due Date / Trigger, Recurrence, Penalty for Breach, Severity.
   - Filter by: "Upcoming in 30 Days", "Financial", "Legal", "Critical Only".
   - One-click "Sync to Google Calendar / iCal" export trigger.

7. Audit & Observability Modal:
   - Displays real-time token utilization, estimated model cost, LLM latency graph, and PII anonymization status to satisfy hackathon judge audit requirements.

================================================================================
2. COMPONENT ARCHITECTURE & DIRECTORY STRUCTURE
================================================================================
frontend/
├── app/
│   ├── layout.tsx                  # Root layout with ThemeProvider, QueryClient, Toaster
│   ├── page.tsx                    # Landing & Contract Upload Hub
│   ├── contracts/
│   │   └── [id]/
│   │       ├── page.tsx            # Main Studio (Redline Viewer + Live Debate)
│   │       ├── risks/page.tsx      # Risk Scorecard View
│   │       └── obligations/page.tsx# Obligations Table & Calendar View
│   ├── audit/page.tsx              # Judge Verification & Token Metrics Dashboard
│   └── globals.css
├── components/
│   ├── ui/                         # shadcn/ui components (button, card, dialog, tabs, badge, table, tooltip, dropdown)
│   ├── layout/
│   │   ├── header.tsx
│   │   ├── sidebar.tsx
│   │   └── token-counter-pill.tsx
│   ├── upload/
│   │   ├── dropzone.tsx
│   │   └── playbook-selector.tsx
│   ├── redline/
│   │   ├── redline-viewer.tsx      # Core Diff Viewer (Unified & Split modes)
│   │   ├── clause-card.tsx         # Individual clause editor with Accept/Reject
│   │   ├── rationale-popover.tsx   # Displays legal precedent & agent rationale
│   │   └── export-menu.tsx
│   ├── agents/
│   │   ├── debate-feed.tsx         # Live SSE multi-agent debate stream
│   │   └── agent-status-badge.tsx
│   ├── risks/
│   │   ├── risk-gauge.tsx          # Animated SVG risk score dial
│   │   └── risk-category-card.tsx
│   └── obligations/
│       ├── obligations-table.tsx   # TanStack table with filtering & sorting
│       └── calendar-export-btn.tsx
├── lib/
│   ├── api.ts                      # Axios / fetch wrapper for backend endpoints
│   ├── sse.ts                      # Server-Sent Events listener for agent stream
│   ├── types.ts                    # Full TypeScript types matching backend schemas
│   └── utils.ts                    # cn helper, currency/date formatters
├── public/
├── package.json
├── tailwind.config.js
└── tsconfig.json

================================================================================
3. TYPESCRIPT DATA CONTRACTS (Matching Backend)
================================================================================
Ensure the frontend strictly implements these types in `lib/types.ts`:

```typescript
export interface RedlineChange {
  id: string;
  sectionNumber: string;
  originalText: string;
  suggestedText: string;
  diffType: 'INSERT' | 'DELETE' | 'REPLACE';
  riskSeverity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  legalRationale: string;
  accepted: boolean | null;
}

export interface ObligationItem {
  id: string;
  clauseReference: string;
  obligor: string;
  recipient: string;
  obligationType: string;
  description: string;
  dueDateOrTrigger: string;
  recurrence: string;
  penaltyForBreach: string;
  isCritical: boolean;
}

export interface ContractAnalysisResult {
  contractId: string;
  fileName: string;
  uploadedAt: string;
  overallRiskScore: number;
  playbookName: string;
  redlines: RedlineChange[];
  obligations: ObligationItem[];
  riskSummary: {
    criticalCount: number;
    highCount: number;
    mediumCount: number;
    lowCount: number;
  };
}

export interface AgentDebateMessage {
  agentName: 'Auditor Agent' | 'Opposing Counsel' | 'Redline Synthesizer';
  timestamp: string;
  content: string;
  targetClause?: string;
}
```

================================================================================
4. DELIVERABLE INSTRUCTIONS
================================================================================
Generate the complete Next.js 14+ frontend application. Write out all components in full detail, ensuring that when the user opens the application, they experience a cohesive, ultra-modern legal tech UI that connects seamlessly to the backend API and provides live visual feedback during multi-agent analysis.
