"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowLeft, Activity, Zap, DollarSign, Clock, ShieldCheck, RefreshCw } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { getAuditSummary } from "@/lib/api";
import { AuditSummary } from "@/lib/types";
import { formatCurrency, formatDate } from "@/lib/utils";

export default function AuditMetricsPage() {
  const [summary, setSummary] = useState<AuditSummary | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchAuditData = () => {
    setLoading(true);
    getAuditSummary()
      .then(setSummary)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchAuditData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header bar */}
      <div className="flex items-center justify-between pb-4 border-b border-gray-800">
        <div className="flex items-center space-x-3">
          <Link
            href="/"
            className="h-8 w-8 rounded-lg bg-gray-900 border border-gray-800 flex items-center justify-center text-gray-400 hover:text-white"
          >
            <ArrowLeft className="h-4 w-4" />
          </Link>
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              Observability, Tokens & Compliance Dashboard
              <Badge variant="outline" className="text-xs bg-blue-950/40 text-blue-400 border-blue-800 font-normal">
                AI Builders Congress Telemetry
              </Badge>
            </h2>
            <p className="text-xs text-gray-400">
              Live token consumption, cost accounting, and guardrails validation for judge review.
            </p>
          </div>
        </div>

        <button
          onClick={fetchAuditData}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-900 border border-gray-800 text-xs text-gray-300 hover:text-white hover:bg-gray-800 transition-colors"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${loading ? "animate-spin" : ""}`} />
          <span>Refresh Metrics</span>
        </button>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-xl border border-gray-800 bg-gray-900/60 space-y-1">
          <div className="flex items-center justify-between text-gray-400 text-xs">
            <span>Total Executions</span>
            <Activity className="h-4 w-4 text-blue-400" />
          </div>
          <p className="text-2xl font-bold font-mono text-white">
            {summary?.total_executions || 0}
          </p>
          <span className="text-[11px] text-gray-500">Autonomous agent passes</span>
        </div>

        <div className="p-5 rounded-xl border border-gray-800 bg-gray-900/60 space-y-1">
          <div className="flex items-center justify-between text-gray-400 text-xs">
            <span>Tokens Consumed</span>
            <Zap className="h-4 w-4 text-indigo-400" />
          </div>
          <p className="text-2xl font-bold font-mono text-indigo-400">
            {summary?.total_tokens_consumed.toLocaleString() || 0}
          </p>
          <span className="text-[11px] text-gray-500">Prompt & completion sum</span>
        </div>

        <div className="p-5 rounded-xl border border-gray-800 bg-gray-900/60 space-y-1">
          <div className="flex items-center justify-between text-gray-400 text-xs">
            <span>Estimated Cloud Cost</span>
            <DollarSign className="h-4 w-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold font-mono text-emerald-400">
            {formatCurrency(summary?.total_cost_usd || 0)}
          </p>
          <span className="text-[11px] text-gray-500">Multi-provider billing model</span>
        </div>

        <div className="p-5 rounded-xl border border-gray-800 bg-gray-900/60 space-y-1">
          <div className="flex items-center justify-between text-gray-400 text-xs">
            <span>Avg Agent Latency</span>
            <Clock className="h-4 w-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold font-mono text-amber-400">
            {summary?.average_latency_ms || 0} ms
          </p>
          <span className="text-[11px] text-gray-500">Fast StateGraph step response</span>
        </div>
      </div>

      {/* Guardrails Verification Banner */}
      <div className="p-4 rounded-xl border border-emerald-900/50 bg-emerald-950/20 flex items-start space-x-3">
        <ShieldCheck className="h-5 w-5 text-emerald-400 shrink-0 mt-0.5" />
        <div className="text-xs space-y-1">
          <h4 className="font-semibold text-emerald-300">Privacy & PII Sanitization Guardrails Active</h4>
          <p className="text-gray-300 leading-relaxed">
            All ingested contracts pass through the regex PII anonymizer (`pii_redactor.py`) prior to vector indexing and LLM prompt generation. Social security numbers, banking credentials, and tax IDs are sanitized at runtime.
          </p>
        </div>
      </div>

      {/* Audit Logs Table */}
      <div className="space-y-3">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-gray-400">
          Recent Agent Invocations & Telemetry Logs
        </h3>

        <div className="overflow-x-auto rounded-xl border border-gray-800 bg-gray-900/50">
          <table className="w-full text-left text-xs">
            <thead className="bg-gray-950/80 border-b border-gray-800 text-gray-400 uppercase font-mono tracking-wider text-[11px]">
              <tr>
                <th className="px-5 py-3.5">Agent Name</th>
                <th className="px-5 py-3.5">Action</th>
                <th className="px-5 py-3.5">Model Engine</th>
                <th className="px-5 py-3.5">Total Tokens</th>
                <th className="px-5 py-3.5">Latency</th>
                <th className="px-5 py-3.5">Cost (USD)</th>
                <th className="px-5 py-3.5">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800/60 font-mono">
              {!summary?.recent_logs || summary.recent_logs.length === 0 ? (
                <tr>
                  <td colSpan={7} className="text-center py-10 text-gray-500">
                    No telemetry execution records captured yet.
                  </td>
                </tr>
              ) : (
                summary.recent_logs.map((log) => (
                  <tr key={log.id} className="hover:bg-gray-800/40 transition-colors">
                    <td className="px-5 py-3 font-semibold text-white font-sans">
                      {log.agent_name}
                    </td>
                    <td className="px-5 py-3 text-gray-300">{log.action}</td>
                    <td className="px-5 py-3 text-indigo-400">{log.model_name}</td>
                    <td className="px-5 py-3 text-gray-300">{log.total_tokens.toLocaleString()}</td>
                    <td className="px-5 py-3 text-amber-400">{log.latency_ms} ms</td>
                    <td className="px-5 py-3 text-emerald-400">${log.cost_usd.toFixed(6)}</td>
                    <td className="px-5 py-3 text-gray-500 text-[11px]">
                      {formatDate(log.timestamp)}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
