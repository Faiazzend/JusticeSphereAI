"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Scale, FileText, ArrowRight, ShieldCheck, Zap, Bot, Clock, Sparkles, AlertTriangle, CheckCircle2 } from "lucide-react";
import { Dropzone } from "@/components/upload/dropzone";
import { listContracts } from "@/lib/api";
import { ContractDetail } from "@/lib/types";
import { formatDate } from "@/lib/utils";

export default function HomePage() {
  const [recentContracts, setRecentContracts] = useState<ContractDetail[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listContracts()
      .then((data) => setRecentContracts(data))
      .catch(() => setRecentContracts([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-10">
      {/* Hero Header */}
      <div className="text-center space-y-3 max-w-2xl mx-auto pt-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/25 text-blue-400 text-xs font-medium">
          <Sparkles className="h-3.5 w-3.5 text-blue-400 animate-spin" />
          <span>Multi-Agent Legal Synthesis & Redlining</span>
        </div>
        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white leading-tight">
          Automated Contract Review &{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400">
            Negotiation Engine
          </span>
        </h1>
        <p className="text-xs sm:text-sm text-gray-400 max-w-xl mx-auto leading-relaxed">
          Simulate opposing counsel pushback, audit compliance against corporate playbooks, generate Word Track Changes, and extract calendar obligations.
        </p>
      </div>

      {/* Main Ingestion & Benchmark Hub */}
      <Dropzone />

      {/* 3-Pillar Capability Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-5xl mx-auto pt-2">
        <div className="p-4 rounded-xl border border-white/5 bg-gray-950/40 hover:border-blue-500/30 transition-all space-y-2">
          <div className="h-8 w-8 rounded-lg bg-blue-500/10 border border-blue-500/25 flex items-center justify-center text-blue-400">
            <Bot className="h-4 w-4" />
          </div>
          <h4 className="text-xs font-bold text-white uppercase tracking-wider">Multi-Agent Debate</h4>
          <p className="text-xs text-gray-400 leading-relaxed">
            Auditor Agent and Opposing Counsel debate clauses to produce market-aligned consensus compromises.
          </p>
        </div>

        <div className="p-4 rounded-xl border border-white/5 bg-gray-950/40 hover:border-indigo-500/30 transition-all space-y-2">
          <div className="h-8 w-8 rounded-lg bg-indigo-500/10 border border-indigo-500/25 flex items-center justify-center text-indigo-400">
            <ShieldCheck className="h-4 w-4" />
          </div>
          <h4 className="text-xs font-bold text-white uppercase tracking-wider">Contextual RAG</h4>
          <p className="text-xs text-gray-400 leading-relaxed">
            Preserves tabular fee schedules and complex multi-page covenant hierarchies without hallucination.
          </p>
        </div>

        <div className="p-4 rounded-xl border border-white/5 bg-gray-950/40 hover:border-emerald-500/30 transition-all space-y-2">
          <div className="h-8 w-8 rounded-lg bg-emerald-500/10 border border-emerald-500/25 flex items-center justify-center text-emerald-400">
            <Scale className="h-4 w-4" />
          </div>
          <h4 className="text-xs font-bold text-white uppercase tracking-wider">Track Changes & JSON</h4>
          <p className="text-xs text-gray-400 leading-relaxed">
            Exports directly to native Word (.docx) with revisions and structured milestone dates for legal operations.
          </p>
        </div>
      </div>

      {/* Recent Contract Audits Feed */}
      <div className="max-w-5xl mx-auto pt-4 space-y-3">
        <div className="flex items-center justify-between pb-1">
          <div className="flex items-center gap-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-gray-300">
              Analyzed Documents
            </h3>
            <span className="text-[11px] px-2 py-0.2 rounded-full bg-gray-800 text-gray-400 font-mono">
              {recentContracts.length}
            </span>
          </div>
          <span className="text-xs text-gray-500 font-mono">
            Click any review to open Interactive Studio
          </span>
        </div>

        {loading ? (
          <div className="p-8 text-center text-xs text-gray-500 font-mono">
            Loading recent contract records...
          </div>
        ) : recentContracts.length === 0 ? (
          <div className="p-8 text-center rounded-xl border border-dashed border-gray-800 bg-gray-950/30 text-xs text-gray-400">
            No contracts analyzed yet. Select a sample above or drop a PDF to initiate review.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {recentContracts.map((c) => (
              <Link
                key={c.id}
                href={`/contracts/${c.id}`}
                className="p-3.5 rounded-xl border border-white/5 bg-gray-950/50 hover:border-blue-500/40 hover:bg-gray-900/60 transition-all flex items-center justify-between group"
              >
                <div className="flex items-center space-x-3 truncate">
                  <div className="h-9 w-9 rounded-lg bg-gray-900 border border-gray-800 flex items-center justify-center text-gray-400 group-hover:text-blue-400 shrink-0 transition-colors">
                    <FileText className="h-4 w-4" />
                  </div>
                  <div className="truncate">
                    <h4 className="text-xs font-semibold text-white group-hover:text-blue-300 transition-colors truncate">
                      {c.title}
                    </h4>
                    <div className="flex items-center space-x-2 text-[10px] text-gray-400 mt-0.5 font-mono">
                      <span className="truncate">{c.playbook_name}</span>
                      <span>&bull;</span>
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        {formatDate(c.created_at)}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-2.5 shrink-0 pl-3">
                  <span
                    className={`text-[11px] font-mono font-bold px-2 py-0.5 rounded-md ${
                      c.overall_risk_score >= 70
                        ? "bg-red-950 text-red-400 border border-red-800/80"
                        : c.overall_risk_score >= 40
                        ? "bg-amber-950 text-amber-400 border border-amber-800/80"
                        : "bg-emerald-950 text-emerald-400 border border-emerald-800/80"
                    }`}
                  >
                    Risk: {c.overall_risk_score}
                  </span>
                  <ArrowRight className="h-3.5 w-3.5 text-gray-600 group-hover:text-blue-400 transition-colors" />
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
