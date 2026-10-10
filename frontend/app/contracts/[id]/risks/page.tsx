"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, RefreshCw, AlertCircle } from "lucide-react";
import { RiskGauge } from "@/components/risks/risk-gauge";
import { RiskCategoryCard } from "@/components/risks/risk-category-card";
import { getContract } from "@/lib/api";
import { ContractDetail } from "@/lib/types";

export default function ContractRisksPage() {
  const params = useParams();
  const contractId = params?.id as string;
  const [contract, setContract] = useState<ContractDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (contractId) {
      getContract(contractId)
        .then(setContract)
        .finally(() => setLoading(false));
    }
  }, [contractId]);

  if (loading) {
    return (
      <div className="h-[60vh] flex items-center justify-center">
        <RefreshCw className="h-6 w-6 text-blue-500 animate-spin" />
      </div>
    );
  }

  if (!contract) return <div>Contract not found</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-3 pb-4 border-b border-gray-800">
        <Link
          href={`/contracts/${contractId}`}
          className="h-8 w-8 rounded-lg bg-gray-900 border border-gray-800 flex items-center justify-center text-gray-400 hover:text-white"
        >
          <ArrowLeft className="h-4 w-4" />
        </Link>
        <div>
          <h2 className="text-xl font-bold text-white">Risk Exposure Analysis</h2>
          <p className="text-xs text-gray-400">{contract.title}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <RiskGauge score={contract.overall_risk_score} />
        </div>
        <div className="lg:col-span-2 space-y-3">
          {contract.redlines.map((rl) => (
            <RiskCategoryCard
              key={rl.id}
              category={rl.diff_type}
              severity={rl.risk_severity}
              score={rl.risk_severity === "CRITICAL" ? 85 : 60}
              rationale={rl.legal_rationale}
              mitigation={rl.suggested_text}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
