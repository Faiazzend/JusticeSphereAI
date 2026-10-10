"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Scale, Terminal, ShieldAlert, Calendar, FileText, RefreshCw, AlertCircle } from "lucide-react";
import { RedlineViewer } from "@/components/redline/redline-viewer";
import { DebateFeed } from "@/components/agents/debate-feed";
import { RiskGauge } from "@/components/risks/risk-gauge";
import { RiskCategoryCard } from "@/components/risks/risk-category-card";
import { ObligationsTable } from "@/components/obligations/obligations-table";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { getContract } from "@/lib/api";
import { ContractDetail } from "@/lib/types";

export default function ContractStudioPage() {
  const params = useParams();
  const contractId = params?.id as string;

  const [contract, setContract] = useState<ContractDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDetails = async () => {
    try {
      setLoading(true);
      const data = await getContract(contractId);
      setContract(data);
    } catch (err: any) {
      setError(err.message || "Failed to load contract");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (contractId) {
      fetchDetails();
    }
  }, [contractId]);

  if (loading) {
    return (
      <div className="h-[60vh] flex flex-col items-center justify-center space-y-3">
        <RefreshCw className="h-8 w-8 text-blue-500 animate-spin" />
        <p className="text-sm text-gray-400 font-mono">Loading Contract Studio...</p>
      </div>
    );
  }

  if (error || !contract) {
    return (
      <div className="max-w-md mx-auto my-16 p-6 rounded-xl border border-red-800 bg-red-950/30 text-center space-y-4">
        <AlertCircle className="h-10 w-10 text-red-400 mx-auto" />
        <h3 className="text-base font-semibold text-white">Error Loading Contract</h3>
        <p className="text-xs text-gray-400">{error || "Contract not found"}</p>
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-xs text-blue-400 hover:text-blue-300"
        >
          <ArrowLeft className="h-3.5 w-3.5" /> Return to Ingestion Hub
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Breadcrumb & Metadata Header */}
      <div className="p-4 rounded-2xl glass-panel flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center space-x-3.5 truncate">
          <Link
            href="/"
            className="h-9 w-9 rounded-xl bg-gray-900/80 border border-white/10 flex items-center justify-center text-gray-400 hover:text-white hover:bg-gray-800 transition-all shadow-sm"
          >
            <ArrowLeft className="h-4 w-4" />
          </Link>
          <div className="truncate">
            <div className="flex items-center gap-2">
              <h2 className="text-lg sm:text-xl font-bold tracking-tight text-white truncate">
                {contract.title}
              </h2>
              <span className="text-[11px] px-2 py-0.5 rounded-full bg-blue-500/15 text-blue-400 border border-blue-500/30 font-medium">
                {contract.playbook_name}
              </span>
            </div>
            <p className="text-[11px] text-gray-400 font-mono mt-0.5">
              File: {contract.original_filename} &bull; ID: {contract.id.slice(0, 8)}
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 text-xs font-mono bg-black/40 px-3.5 py-1.5 rounded-xl border border-white/10">
            <span className="text-gray-400">Risk Severity:</span>
            <span
              className={`font-bold ${
                contract.overall_risk_score >= 70
                  ? "text-red-400"
                  : contract.overall_risk_score >= 40
                  ? "text-amber-400"
                  : "text-emerald-400"
              }`}
            >
              {contract.overall_risk_score}/100
            </span>
          </div>

          <Badge variant="outline" className="text-xs font-mono bg-emerald-950/40 text-emerald-400 border-emerald-800/80 rounded-xl px-2.5 py-1">
            Status: {contract.status.toUpperCase()}
          </Badge>
        </div>
      </div>

      {/* Primary Studio Navigation Tabs */}
      <Tabs defaultValue="redlines" className="space-y-5">
        <TabsList className="bg-gray-950/90 border border-white/10 p-1 rounded-xl shadow-lg">
          <TabsTrigger value="redlines" className="flex items-center gap-1.5 text-xs rounded-lg data-[state=active]:bg-blue-600 data-[state=active]:text-white">
            <Scale className="h-3.5 w-3.5" />
            <span>Redlines ({contract.redlines.length})</span>
          </TabsTrigger>

          <TabsTrigger value="debate" className="flex items-center gap-1.5 text-xs rounded-lg data-[state=active]:bg-indigo-600 data-[state=active]:text-white">
            <Terminal className="h-3.5 w-3.5" />
            <span>Agent Debate ({contract.debate_transcript.length})</span>
          </TabsTrigger>

          <TabsTrigger value="risks" className="flex items-center gap-1.5 text-xs rounded-lg data-[state=active]:bg-amber-600 data-[state=active]:text-white">
            <ShieldAlert className="h-3.5 w-3.5" />
            <span>Risk Scorecard</span>
          </TabsTrigger>

          <TabsTrigger value="obligations" className="flex items-center gap-1.5 text-xs rounded-lg data-[state=active]:bg-emerald-600 data-[state=active]:text-white">
            <Calendar className="h-3.5 w-3.5" />
            <span>Obligations Matrix ({contract.obligations.length})</span>
          </TabsTrigger>
        </TabsList>

        {/* Tab 1: Redline Studio */}
        <TabsContent value="redlines">
          <RedlineViewer
            contractId={contract.id}
            contractTitle={contract.title}
            redlines={contract.redlines}
            obligations={contract.obligations}
          />
        </TabsContent>

        {/* Tab 2: Multi-Agent Debate Feed */}
        <TabsContent value="debate">
          <DebateFeed
            contractId={contract.id}
            initialMessages={contract.debate_transcript}
          />
        </TabsContent>

        {/* Tab 3: Risk Scorecard & Matrix */}
        <TabsContent value="risks">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-1">
              <RiskGauge score={contract.overall_risk_score} />
            </div>

            <div className="lg:col-span-2 space-y-4">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-gray-400">
                Categorized Exposure Analysis
              </h4>
              <div className="space-y-3">
                {contract.redlines.map((rl) => (
                  <RiskCategoryCard
                    key={rl.id}
                    category={rl.diff_type}
                    severity={rl.risk_severity}
                    score={
                      rl.risk_severity === "CRITICAL"
                        ? 85
                        : rl.risk_severity === "HIGH"
                        ? 70
                        : 45
                    }
                    rationale={rl.legal_rationale}
                    mitigation={rl.suggested_text}
                  />
                ))}
              </div>
            </div>
          </div>
        </TabsContent>

        {/* Tab 4: Obligations & Calendar */}
        <TabsContent value="obligations">
          <ObligationsTable
            contractTitle={contract.title}
            obligations={contract.obligations}
          />
        </TabsContent>
      </Tabs>
    </div>
  );
}
