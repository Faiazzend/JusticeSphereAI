export type DiffTokenType = 'equal' | 'insert' | 'delete' | 'replace';

export interface DiffToken {
  type: DiffTokenType;
  text: string;
}

export interface RedlineChange {
  id: string;
  section_number: string;
  original_text: string;
  suggested_text: string;
  diff_type: 'INSERT' | 'DELETE' | 'REPLACE';
  risk_severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  legal_rationale: string;
  diff_tokens?: DiffToken[];
  accepted: boolean | null;
}

export interface ObligationItem {
  id: string;
  clause_reference: string;
  obligor: string;
  recipient: string;
  obligation_type: string;
  description: string;
  due_date_or_trigger: string;
  recurrence: string;
  penalty_for_breach: string;
  is_critical: boolean;
}

export interface RiskSummary {
  overall_score: number;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  category_scores?: Record<string, number>;
}

export interface AgentDebateMessage {
  index?: number;
  agent_name: 'Auditor Agent' | 'Opposing Counsel' | 'Redline Synthesizer' | string;
  timestamp: string;
  content: string;
  target_clause?: string;
}

export interface ContractDetail {
  id: string;
  title: string;
  original_filename: string;
  status: 'uploaded' | 'processing' | 'analyzed' | 'error';
  error_message?: string;
  playbook_name: string;
  overall_risk_score: number;
  risk_summary: RiskSummary;
  redlines: RedlineChange[];
  obligations: ObligationItem[];
  debate_transcript: AgentDebateMessage[];
  created_at: string;
  updated_at: string;
}

export interface PlaybookRule {
  category: string;
  standard_requirement: string;
  unacceptable_terms: string[];
  preferred_fallback: string;
  severity_if_missing: string;
}

export interface Playbook {
  id: string;
  name: string;
  description: string;
  rules: PlaybookRule[];
  is_default: boolean;
  created_at: string;
}

export interface AuditLogItem {
  id: string;
  contract_id: string | null;
  agent_name: string;
  action: string;
  model_name: string;
  total_tokens: number;
  latency_ms: number;
  cost_usd: number;
  timestamp: string;
}

export interface AuditSummary {
  total_executions: number;
  total_tokens_consumed: number;
  total_cost_usd: number;
  average_latency_ms: number;
  recent_logs: AuditLogItem[];
}
