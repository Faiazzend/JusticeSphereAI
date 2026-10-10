import { ContractDetail, Playbook, AuditSummary, ObligationItem, RedlineChange } from './types';

export function getApiBase(): string {
  if (typeof window !== 'undefined') {
    if (process.env.NEXT_PUBLIC_API_URL) {
      return `${process.env.NEXT_PUBLIC_API_URL}/api/v1`;
    }
    const host = window.location.hostname || '127.0.0.1';
    return `http://${host}:8000/api/v1`;
  }
  return process.env.NEXT_PUBLIC_API_URL 
    ? `${process.env.NEXT_PUBLIC_API_URL}/api/v1` 
    : 'http://127.0.0.1:8000/api/v1';
}

export function getBackendBase(): string {
  if (typeof window !== 'undefined') {
    if (process.env.NEXT_PUBLIC_API_URL) {
      return process.env.NEXT_PUBLIC_API_URL;
    }
    const host = window.location.hostname || '127.0.0.1';
    return `http://${host}:8000`;
  }
  return process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
}

export async function uploadContract(
  file: File, 
  title?: string, 
  playbookName?: string
): Promise<{ id: string; title: string }> {
  const formData = new FormData();
  formData.append('file', file);
  if (title && title.trim()) formData.append('title', title.trim());
  if (playbookName) formData.append('playbook_name', playbookName);

  const apiBase = getApiBase();
  let res: Response;

  try {
    res = await fetch(`${apiBase}/contracts/upload`, {
      method: 'POST',
      body: formData,
    });
  } catch (err: any) {
    throw new Error(
      `Cannot connect to ContractMind backend at ${apiBase}. ` +
      `Please ensure the backend is running on port 8000. (Network details: ${err.message || 'Connection refused'})`
    );
  }

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Upload failed with HTTP ${res.status}: ${res.statusText}`);
  }

  return res.json();
}

export async function loadDemoContract(
  sampleType: 'msa' | 'saas' | 'nda' | 'ma' | 'cloud_dpa' | 'joint_ip'
): Promise<{ id: string; title: string }> {
  const apiBase = getApiBase();
  let res: Response;
  try {
    res = await fetch(`${apiBase}/contracts/demo/${sampleType}`, {
      method: 'POST',
    });
  } catch (err: any) {
    throw new Error(`Demo launcher failed to reach backend at ${apiBase}: ${err.message}`);
  }

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Demo load failed with status ${res.status}`);
  }

  return res.json();
}

export async function listContracts(): Promise<ContractDetail[]> {
  const apiBase = getApiBase();
  try {
    const res = await fetch(`${apiBase}/contracts/`, { cache: 'no-store' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  } catch {
    return [];
  }
}

export async function getContract(contractId: string): Promise<ContractDetail> {
  const apiBase = getApiBase();
  let res: Response;
  try {
    res = await fetch(`${apiBase}/contracts/${contractId}`, { cache: 'no-store' });
  } catch (err: any) {
    throw new Error(`Cannot reach backend at ${apiBase}: ${err.message}`);
  }

  if (!res.ok) throw new Error('Contract not found or analysis pending');
  return res.json();
}

export async function deleteContract(contractId: string): Promise<void> {
  const apiBase = getApiBase();
  const res = await fetch(`${apiBase}/contracts/${contractId}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete contract');
}

export async function triggerAnalysis(
  contractId: string, 
  playbookName: string = 'Standard Corporate Playbook',
  useLocalLLM: boolean = false,
  llmProvider?: string,
  modelName?: string,
  apiKey?: string
): Promise<{ message: string; contract_id: string; overall_risk_score: number }> {
  const apiBase = getApiBase();
  let res: Response;
  try {
    res = await fetch(`${apiBase}/analysis/${contractId}/trigger`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        playbook_name: playbookName, 
        use_local_llm: useLocalLLM,
        llm_provider: llmProvider,
        model_name: modelName,
        api_key: apiKey
      }),
    });
  } catch (err: any) {
    throw new Error(`Analysis engine connection failed at ${apiBase}: ${err.message}`);
  }

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Analysis execution failed');
  }

  return res.json();
}

export async function updateRedlineDecision(
  contractId: string, 
  redlineId: string, 
  accepted: boolean | null
): Promise<void> {
  const apiBase = getApiBase();
  const res = await fetch(`${apiBase}/analysis/${contractId}/redlines/${redlineId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ accepted }),
  });

  if (!res.ok) throw new Error('Failed to update redline decision');
}

export async function getObligations(contractId: string): Promise<{ obligations: ObligationItem[] }> {
  const apiBase = getApiBase();
  const res = await fetch(`${apiBase}/analysis/${contractId}/obligations`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch obligations');
  return res.json();
}

export async function listPlaybooks(): Promise<Playbook[]> {
  const apiBase = getApiBase();
  try {
    const res = await fetch(`${apiBase}/playbooks/`, { cache: 'no-store' });
    if (!res.ok) return [];
    return res.json();
  } catch {
    return [];
  }
}

export async function getAuditSummary(): Promise<AuditSummary> {
  const apiBase = getApiBase();
  try {
    const res = await fetch(`${apiBase}/analysis/audit/summary`, { cache: 'no-store' });
    if (!res.ok) {
      return { total_executions: 0, total_tokens_consumed: 0, total_cost_usd: 0, average_latency_ms: 0, recent_logs: [] };
    }
    return res.json();
  } catch {
    return { total_executions: 0, total_tokens_consumed: 0, total_cost_usd: 0, average_latency_ms: 0, recent_logs: [] };
  }
}

export function getExportDocxUrl(contractId: string): string {
  const apiBase = getApiBase();
  return `${apiBase}/analysis/${contractId}/export/docx`;
}

export async function getMCPTools(): Promise<{ tools: any[] }> {
  try {
    const backendBase = getBackendBase();
    const res = await fetch(`${backendBase}/mcp/tools`, { cache: 'no-store' });
    if (!res.ok) return { tools: [] };
    return res.json();
  } catch {
    return { tools: [] };
  }
}

export interface LLMConfig {
  gemini_configured: boolean;
  openai_configured: boolean;
  anthropic_configured: boolean;
  ollama_available: boolean;
  ollama_base_url: string;
  ollama_models: string[];
  default_model: string;
  fallback_model: string;
}

export async function getLLMConfig(): Promise<LLMConfig> {
  const apiBase = getApiBase();
  try {
    const res = await fetch(`${apiBase}/analysis/llm/config`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch LLM config');
    return res.json();
  } catch {
    return {
      gemini_configured: false,
      openai_configured: false,
      anthropic_configured: false,
      ollama_available: false,
      ollama_base_url: 'http://localhost:11434',
      ollama_models: [],
      default_model: 'gemini-3.5-flash-lite',
      fallback_model: 'deepseek-r1:latest'
    };
  }
}

export async function updateLLMConfig(payload: {
  gemini_api_key?: string;
  openai_api_key?: string;
  anthropic_api_key?: string;
  default_model?: string;
}): Promise<any> {
  const apiBase = getApiBase();
  const res = await fetch(`${apiBase}/analysis/llm/config`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to update LLM configuration');
  return res.json();
}
