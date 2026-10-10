"use client";

import React, { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { UploadCloud, FileText, CheckCircle2, AlertCircle, Loader2, ArrowRight, Sparkles, ShieldAlert, Rocket, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PlaybookSelector } from "./playbook-selector";
import { ModelProviderSelector, AIProviderState } from "./model-provider-selector";
import { uploadContract, triggerAnalysis, loadDemoContract } from "@/lib/api";

const STEPS = [
  "Ingesting & extracting document structure via PyMuPDF...",
  "Indexing Contextual RAG chunks into Vector Store...",
  "Running Auditor Agent compliance scan against Playbook...",
  "Simulating Opposing Counsel negotiation & counter-clauses...",
  "Synthesizing consensus redlines & extracting obligations JSON..."
];

export function Dropzone() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState<string>("");
  const [playbook, setPlaybook] = useState<string>("Standard Corporate Playbook");
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [demoLoading, setDemoLoading] = useState<string | null>(null);
  const [aiProvider, setAiProvider] = useState<AIProviderState>({
    provider: "gemini",
    modelName: "gemini-3.5-flash-lite",
    apiKey: "",
    useLocalLLM: false,
  });
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.name.toLowerCase().endsWith(".pdf")) {
        setFile(droppedFile);
        if (!title) setTitle(droppedFile.name.replace(/\.[^/.]+$/, ""));
        setError(null);
      } else {
        setError("Only PDF contract documents are accepted.");
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      if (selected.name.toLowerCase().endsWith(".pdf")) {
        setFile(selected);
        if (!title) setTitle(selected.name.replace(/\.[^/.]+$/, ""));
        setError(null);
      } else {
        setError("Only PDF contract documents are accepted.");
      }
    }
  };

  const handleUploadAndAnalyze = async () => {
    if (!file) return;

    try {
      setUploading(true);
      setError(null);
      setCurrentStepIndex(0);

      const stepInterval = setInterval(() => {
        setCurrentStepIndex((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
      }, 900);

      // 1. Ingest PDF
      const res = await uploadContract(file, title, playbook);

      // 2. Trigger Multi-Agent Workflow with selected model provider
      await triggerAnalysis(
        res.id,
        playbook,
        aiProvider.useLocalLLM,
        aiProvider.provider,
        aiProvider.modelName,
        aiProvider.apiKey
      );

      clearInterval(stepInterval);
      router.push(`/contracts/${res.id}`);
    } catch (err: any) {
      setError(err.message || "Failed to process contract");
      setUploading(false);
    }
  };

  const handleLaunchDemo = async (type: 'msa' | 'saas' | 'nda' | 'ma' | 'cloud_dpa' | 'joint_ip') => {
    try {
      setDemoLoading(type);
      setError(null);
      const res = await loadDemoContract(type);
      router.push(`/contracts/${res.id}`);
    } catch (err: any) {
      setError(err.message || "Failed to load sample benchmark");
      setDemoLoading(null);
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto space-y-5">
      {/* Active AI Model Indicator Strip */}
      <div className="flex items-center justify-between px-4 py-2.5 rounded-xl bg-base-200/60 border border-white/5 text-xs shadow-sm">
        <div className="flex items-center space-x-2.5">
          <span className="badge badge-success badge-xs animate-pulse"></span>
          <span className="text-gray-400">Inference Core:</span>
          <span className="font-semibold text-gray-100 font-mono">
            {aiProvider.provider === "gemini" ? "Google Gemini (3.5 Flash Lite)" :
             aiProvider.provider === "ollama" ? "Local Ollama Engine" :
             aiProvider.provider === "openai" ? "OpenAI / Codex (gpt-4o)" : "Anthropic Claude (3.5 Sonnet)"}
          </span>
        </div>
        <div className="badge badge-neutral badge-sm font-mono text-[10px]">
          {aiProvider.provider === "gemini" ? "Cloud Live • Sub-2s" :
           aiProvider.provider === "ollama" ? (aiProvider.useLocalLLM ? "Local Offline" : "Heuristic Safe Fallback") :
           "API Connected"}
        </div>
      </div>

      {/* Drop Zone Box */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !uploading && fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-300 ${
          isDragging
            ? "border-primary bg-primary/10 shadow-2xl scale-[1.01]"
            : file
            ? "border-success/60 bg-success/5"
            : "border-white/10 bg-base-200/40 hover:border-primary/50 hover:bg-base-200/70"
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={handleFileChange}
        />

        <div className="flex flex-col items-center justify-center space-y-3">
          <div
            className={`h-12 w-12 rounded-xl flex items-center justify-center transition-transform ${
              file ? "bg-success/20 text-success border border-success/40" : "bg-primary/10 text-primary border border-primary/30"
            }`}
          >
            {file ? <CheckCircle2 className="h-6 w-6" /> : <UploadCloud className="h-6 w-6" />}
          </div>

          <div>
            <h4 className="text-sm sm:text-base font-semibold text-white">
              {file ? file.name : "Drop contract PDF here, or click to browse"}
            </h4>
            <p className="text-xs text-gray-400 mt-0.5">
              Analyzes MSAs, SaaS Terms, NDAs, and Vendor Agreements
            </p>
          </div>
        </div>
      </div>

      {/* Progress Stepper during Analysis */}
      {uploading && (
        <div className="alert alert-info bg-info/10 border-info/30 text-xs shadow-md space-y-2 flex flex-col items-start animate-in fade-in-50">
          <div className="flex items-center space-x-2 text-info font-semibold">
            <Loader2 className="h-4 w-4 animate-spin shrink-0" />
            <span>Multi-Agent Legal Synthesis in Progress...</span>
          </div>

          <div className="space-y-1.5 w-full pt-1">
            {STEPS.map((step, idx) => {
              const isPast = idx < currentStepIndex;
              const isCurrent = idx === currentStepIndex;
              return (
                <div key={idx} className="flex items-center space-x-2 text-xs">
                  {isPast ? (
                    <Check className="h-3.5 w-3.5 text-success shrink-0" />
                  ) : isCurrent ? (
                    <span className="badge badge-info badge-xs shrink-0 animate-ping" />
                  ) : (
                    <span className="h-1.5 w-1.5 rounded-full bg-gray-700 shrink-0 ml-1 mr-0.5" />
                  )}
                  <span className={isCurrent ? "text-white font-medium" : isPast ? "text-gray-400 line-through" : "text-gray-600"}>
                    {step}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Contract Title Input & Playbook Selector */}
      {file && !uploading && (
        <div className="space-y-4 animate-in fade-in-50">
          <div>
            <label className="text-xs font-semibold uppercase tracking-wider text-gray-400 block mb-1.5">
              Contract Identification Title
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Acme Corp Enterprise MSA 2026"
              className="input input-bordered w-full bg-base-200 border-white/10 text-gray-100 placeholder-gray-500 text-sm focus:input-primary"
            />
          </div>

          {/* AI Model & Provider Selector */}
          <ModelProviderSelector value={aiProvider} onChange={setAiProvider} />

          {/* Playbook Selector */}
          <PlaybookSelector selected={playbook} onSelect={setPlaybook} />

          {/* Error Message Display */}
          {error && (
            <div className="alert alert-error text-xs shadow-sm">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Action Button & Status */}
          <div className="pt-2">
            <button
              disabled={uploading}
              onClick={handleUploadAndAnalyze}
              className="btn btn-primary w-full h-12 text-sm font-semibold flex items-center justify-center gap-2 shadow-lg shadow-primary/25"
            >
              <span>Ingest & Run Multi-Agent Review</span>
              <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      {/* 1-Click Benchmark Demo Launchers for Instant Testing */}
      {!file && !uploading && (
        <div className="space-y-3 pt-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-gray-300 flex items-center gap-1.5">
              <Sparkles className="h-3.5 w-3.5 text-purple-400" />
              Pre-loaded Test Contracts
            </span>
            <span className="text-[11px] text-gray-400">
              1-click test datasets
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
            {/* Cross-Border M&A */}
            <button
              onClick={() => handleLaunchDemo('ma')}
              disabled={Boolean(demoLoading)}
              className="p-3 rounded-xl border border-red-900/50 bg-red-950/20 hover:bg-red-950/40 hover:border-red-600 transition-all text-left"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-semibold text-red-200">Cross-Border M&A</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-red-900/80 text-red-300 font-mono">
                  Risk: 87
                </span>
              </div>
              <p className="text-[11px] text-gray-400 truncate">
                Tipping baskets & IP trap
              </p>
              {demoLoading === 'ma' && (
                <div className="flex items-center gap-1 text-[10px] text-red-300 mt-1.5 font-mono">
                  <Loader2 className="h-3 w-3 animate-spin" /> Analyzing...
                </div>
              )}
            </button>

            {/* Cloud AI MSA & DPA */}
            <button
              onClick={() => handleLaunchDemo('cloud_dpa')}
              disabled={Boolean(demoLoading)}
              className="p-3 rounded-xl border border-indigo-900/50 bg-indigo-950/20 hover:bg-indigo-950/40 hover:border-indigo-600 transition-all text-left"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-semibold text-indigo-200">Cloud AI & DPA</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-indigo-900/80 text-indigo-300 font-mono">
                  Risk: 79
                </span>
              </div>
              <p className="text-[11px] text-gray-400 truncate">
                Model training on data & SLAs
              </p>
              {demoLoading === 'cloud_dpa' && (
                <div className="flex items-center gap-1 text-[10px] text-indigo-300 mt-1.5 font-mono">
                  <Loader2 className="h-3 w-3 animate-spin" /> Analyzing...
                </div>
              )}
            </button>

            {/* Strategic AI Joint R&D */}
            <button
              onClick={() => handleLaunchDemo('joint_ip')}
              disabled={Boolean(demoLoading)}
              className="p-3 rounded-xl border border-purple-900/50 bg-purple-950/20 hover:bg-purple-950/40 hover:border-purple-600 transition-all text-left"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-semibold text-purple-200">AI Joint R&D</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-purple-900/80 text-purple-300 font-mono">
                  Risk: 83
                </span>
              </div>
              <p className="text-[11px] text-gray-400 truncate">
                Joint IP without accounting
              </p>
              {demoLoading === 'joint_ip' && (
                <div className="flex items-center gap-1 text-[10px] text-purple-300 mt-1.5 font-mono">
                  <Loader2 className="h-3 w-3 animate-spin" /> Analyzing...
                </div>
              )}
            </button>

            {/* Enterprise MSA */}
            <button
              onClick={() => handleLaunchDemo('msa')}
              disabled={Boolean(demoLoading)}
              className="p-3 rounded-xl border border-gray-800 bg-gray-900/40 hover:bg-gray-800/60 hover:border-gray-700 transition-all text-left"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-semibold text-gray-300">Enterprise MSA</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-950 text-amber-300 font-mono">
                  Risk: 65
                </span>
              </div>
              <p className="text-[11px] text-gray-400 truncate">
                Uncapped indemnity & caps
              </p>
              {demoLoading === 'msa' && (
                <div className="flex items-center gap-1 text-[10px] text-gray-300 mt-1.5 font-mono">
                  <Loader2 className="h-3 w-3 animate-spin" /> Analyzing...
                </div>
              )}
            </button>

            {/* SaaS Agreement */}
            <button
              onClick={() => handleLaunchDemo('saas')}
              disabled={Boolean(demoLoading)}
              className="p-3 rounded-xl border border-gray-800 bg-gray-900/40 hover:bg-gray-800/60 hover:border-gray-700 transition-all text-left"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-semibold text-gray-300">SaaS Agreement</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-950 text-amber-300 font-mono">
                  Risk: 50
                </span>
              </div>
              <p className="text-[11px] text-gray-400 truncate">
                Auto-renewal lock-in
              </p>
              {demoLoading === 'saas' && (
                <div className="flex items-center gap-1 text-[10px] text-gray-300 mt-1.5 font-mono">
                  <Loader2 className="h-3 w-3 animate-spin" /> Analyzing...
                </div>
              )}
            </button>

            {/* Mutual NDA */}
            <button
              onClick={() => handleLaunchDemo('nda')}
              disabled={Boolean(demoLoading)}
              className="p-3 rounded-xl border border-gray-800 bg-gray-900/40 hover:bg-gray-800/60 hover:border-gray-700 transition-all text-left"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-semibold text-gray-300">Mutual NDA</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-300 font-mono">
                  Risk: 25
                </span>
              </div>
              <p className="text-[11px] text-gray-400 truncate">
                Confidentiality standard
              </p>
              {demoLoading === 'nda' && (
                <div className="flex items-center gap-1 text-[10px] text-gray-300 mt-1.5 font-mono">
                  <Loader2 className="h-3 w-3 animate-spin" /> Analyzing...
                </div>
              )}
            </button>
          </div>

          {error && (
            <div className="flex items-center space-x-2 text-red-400 bg-red-950/40 border border-red-800/60 p-3 rounded-lg text-xs mt-2">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
