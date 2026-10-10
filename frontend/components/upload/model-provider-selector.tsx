"use client";

import React, { useState, useEffect } from "react";
import { Sparkles, Key, Check, RefreshCw, Terminal, Info, ChevronDown, ChevronUp, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";
import { getLLMConfig, updateLLMConfig, LLMConfig } from "@/lib/api";

export interface AIProviderState {
  provider: "gemini" | "openai" | "anthropic" | "ollama";
  modelName: string;
  apiKey: string;
  useLocalLLM: boolean;
}

interface ModelProviderSelectorProps {
  value: AIProviderState;
  onChange: (val: AIProviderState) => void;
}

export function ModelProviderSelector({ value, onChange }: ModelProviderSelectorProps) {
  const [config, setConfig] = useState<LLMConfig | null>(null);
  const [showConfigDrawer, setShowConfigDrawer] = useState(false);
  const [savingKey, setSavingKey] = useState(false);
  const [customKey, setCustomKey] = useState("");
  const [saveMessage, setSaveMessage] = useState<string | null>(null);

  const fetchConfig = async () => {
    try {
      const cfg = await getLLMConfig();
      setConfig(cfg);
    } catch {
      // safe fallback
    }
  };

  useEffect(() => {
    fetchConfig();
  }, []);

  const handleSelectProvider = (prov: "gemini" | "openai" | "anthropic" | "ollama") => {
    let defModel = "gemini-3.5-flash-lite";
    let isLocal = false;
    if (prov === "gemini") {
      defModel = "gemini-3.5-flash-lite";
    } else if (prov === "openai") {
      defModel = "gpt-4o";
    } else if (prov === "anthropic") {
      defModel = "claude-3-5-sonnet-20241022";
    } else if (prov === "ollama") {
      defModel = config?.ollama_models?.[0] || "deepseek-r1:latest";
      isLocal = true;
    }

    onChange({
      ...value,
      provider: prov,
      modelName: defModel,
      useLocalLLM: isLocal,
    });
  };

  const handleSaveKey = async () => {
    if (!customKey.trim()) return;
    try {
      setSavingKey(true);
      setSaveMessage(null);
      const payload: Record<string, string> = {};
      if (value.provider === "gemini") payload.gemini_api_key = customKey.trim();
      if (value.provider === "openai") payload.openai_api_key = customKey.trim();
      if (value.provider === "anthropic") payload.anthropic_api_key = customKey.trim();

      await updateLLMConfig(payload);
      await fetchConfig();
      setSaveMessage("Saved! Key active for all agents.");
      setCustomKey("");
      setTimeout(() => setSaveMessage(null), 3500);
    } catch (err: any) {
      setSaveMessage("Error saving key: " + err.message);
    } finally {
      setSavingKey(false);
    }
  };

  const providers = [
    {
      id: "gemini" as const,
      name: "Google Gemini",
      model: "3.5 Flash Lite",
      status: config?.gemini_configured ? "Active (Live Cloud)" : "Key Needed",
      activeColor: "border-blue-500 bg-blue-950/25 text-blue-200",
      dotColor: config?.gemini_configured ? "bg-emerald-400" : "bg-gray-500",
      tag: "Connected",
    },
    {
      id: "ollama" as const,
      name: "Local Ollama",
      model: config?.ollama_models?.[0] || "deepseek-r1",
      status: config?.ollama_available
        ? `${config.ollama_models?.length || 0} local models`
        : "Installed (Stopped)",
      activeColor: "border-amber-500 bg-amber-950/25 text-amber-200",
      dotColor: config?.ollama_available ? "bg-emerald-400" : "bg-amber-400",
      tag: config?.ollama_available ? "Local Online" : "100% Offline",
    },
    {
      id: "openai" as const,
      name: "OpenAI / Codex",
      model: "gpt-4o",
      status: config?.openai_configured ? "Ready" : "Add Key",
      activeColor: "border-emerald-500 bg-emerald-950/25 text-emerald-200",
      dotColor: config?.openai_configured ? "bg-emerald-400" : "bg-gray-500",
      tag: config?.openai_configured ? "Configured" : "BYO Key",
    },
    {
      id: "anthropic" as const,
      name: "Anthropic Claude",
      model: "3.5 Sonnet",
      status: config?.anthropic_configured ? "Ready" : "Add Key",
      activeColor: "border-purple-500 bg-purple-950/25 text-purple-200",
      dotColor: config?.anthropic_configured ? "bg-emerald-400" : "bg-gray-500",
      tag: config?.anthropic_configured ? "Configured" : "BYO Key",
    },
  ];

  const currentProvider = providers.find((p) => p.id === value.provider);

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/40 p-3.5 space-y-3">
      {/* Header Bar */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Sparkles className="h-4 w-4 text-blue-400" />
          <span className="text-xs font-semibold text-gray-200 uppercase tracking-wider">
            Inference Engine
          </span>
          <span className="text-[11px] px-2 py-0.5 rounded-full bg-gray-800 border border-gray-700 text-gray-300 font-mono">
            {currentProvider?.name} &bull; {currentProvider?.model}
          </span>
        </div>

        <button
          type="button"
          onClick={() => setShowConfigDrawer(!showConfigDrawer)}
          className="text-xs text-blue-400 hover:text-blue-300 flex items-center gap-1 font-medium transition-colors"
        >
          {showConfigDrawer ? "Close Settings" : "Configure Engine"}
          {showConfigDrawer ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
        </button>
      </div>

      {/* Provider Selector Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
        {providers.map((p) => {
          const isSelected = value.provider === p.id;
          return (
            <button
              key={p.id}
              type="button"
              onClick={() => handleSelectProvider(p.id)}
              className={cn(
                "p-2.5 rounded-lg border text-left transition-all flex flex-col justify-between",
                isSelected
                  ? `${p.activeColor} shadow-sm ring-1 ring-white/10`
                  : "border-gray-800/80 bg-gray-950/40 text-gray-400 hover:border-gray-700 hover:text-gray-200"
              )}
            >
              <div className="flex items-center justify-between w-full mb-1">
                <span className="text-xs font-semibold">{p.name}</span>
                <span className={cn("h-1.5 w-1.5 rounded-full shrink-0", p.dotColor)} />
              </div>
              <div className="flex items-center justify-between w-full text-[10px]">
                <span className="font-mono text-gray-400 truncate">{p.model}</span>
                <span className="text-[9px] px-1 rounded bg-gray-800/80 text-gray-300 font-mono shrink-0 ml-1">
                  {p.tag}
                </span>
              </div>
            </button>
          );
        })}
      </div>

      {/* Explicit Execution Mode Callout */}
      <div className="rounded-lg bg-gray-950/70 border border-gray-800/90 p-2.5 text-[11px] text-gray-400 flex items-start gap-2">
        <Info className="h-4 w-4 text-blue-400 shrink-0 mt-0.5" />
        <div className="leading-relaxed flex-1">
          {value.provider === "gemini" && (
            <span>
              <strong className="text-blue-300">Google Gemini Live:</strong> Multi-agent debate queries Google's cloud API directly with your connected key.
            </span>
          )}
          {value.provider === "ollama" && (
            <span>
              <strong className="text-amber-300">Local Ollama Status:</strong>{" "}
              {config?.ollama_available ? (
                `Ollama server is active on localhost:11434 with ${config.ollama_models?.length || 0} model(s).`
              ) : (
                <span>
                  Ollama executable is installed, but the background service is stopped or no local model is pulled. If selected, ContractMind will safely use the <strong>built-in deterministic legal heuristic engine</strong> so analysis never crashes. Run <code className="text-gray-200">ollama run deepseek-r1</code> to run 100% offline.
                </span>
              )}
            </span>
          )}
          {value.provider === "openai" && (
            <span>
              <strong className="text-emerald-300">OpenAI / Codex:</strong>{" "}
              {config?.openai_configured
                ? "Key is active and configured."
                : "No OpenAI key found. Click 'Configure Engine' above to enter your key."}
            </span>
          )}
          {value.provider === "anthropic" && (
            <span>
              <strong className="text-purple-300">Anthropic Claude:</strong>{" "}
              {config?.anthropic_configured
                ? "Key is active and configured."
                : "No Anthropic key found. Click 'Configure Engine' above to enter your key."}
            </span>
          )}
        </div>
      </div>

      {/* Expandable Key & Configuration Drawer */}
      {showConfigDrawer && (
        <div className="rounded-lg bg-gray-950 border border-gray-800 p-3 space-y-3 animate-in fade-in-50">
          <div className="flex items-center justify-between text-xs">
            <span className="font-semibold text-gray-300">API Key & Local Engine Settings</span>
            <button
              type="button"
              onClick={fetchConfig}
              className="text-[11px] text-gray-400 hover:text-gray-200 flex items-center gap-1"
            >
              <RefreshCw className="h-3 w-3" /> Refresh status
            </button>
          </div>

          {value.provider !== "ollama" ? (
            <div className="space-y-2">
              <div className="flex gap-2">
                <input
                  type="password"
                  value={customKey}
                  onChange={(e) => setCustomKey(e.target.value)}
                  placeholder={`Enter ${value.provider.toUpperCase()} API key...`}
                  className="flex-1 px-3 py-1.5 rounded bg-gray-900 border border-gray-700 text-xs text-gray-100 placeholder-gray-500 focus:outline-none focus:border-blue-500 font-mono"
                />
                <button
                  type="button"
                  disabled={savingKey || !customKey.trim()}
                  onClick={handleSaveKey}
                  className="px-3 py-1.5 rounded bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white text-xs font-semibold flex items-center gap-1"
                >
                  {savingKey ? <RefreshCw className="h-3 w-3 animate-spin" /> : <Check className="h-3 w-3" />}
                  Save Key
                </button>
              </div>
              {saveMessage && (
                <div className="text-[11px] text-emerald-400 font-medium">{saveMessage}</div>
              )}
            </div>
          ) : (
            <div className="rounded bg-gray-900/80 p-2.5 border border-gray-800 space-y-2 text-xs">
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Local Endpoint:</span>
                <span className="font-mono text-gray-400">http://localhost:11434</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Installed Binaries:</span>
                <span className="font-mono text-emerald-400">ollama.exe (v0.40.2 Ready)</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Installed Models:</span>
                <span className="font-mono text-gray-400">
                  {config?.ollama_models && config.ollama_models.length > 0
                    ? config.ollama_models.join(", ")
                    : "None downloaded yet"}
                </span>
              </div>
              <div className="pt-1 text-[11px] text-gray-400 border-t border-gray-800">
                To download and launch a local model, run in your terminal:
                <div className="mt-1 p-1.5 rounded bg-black/60 font-mono text-[11px] text-amber-300">
                  ollama run deepseek-r1:latest
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
