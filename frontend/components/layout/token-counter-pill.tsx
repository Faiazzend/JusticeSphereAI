"use client";

import React, { useEffect, useState } from "react";
import { Zap, DollarSign } from "lucide-react";
import { getAuditSummary } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";

export function TokenCounterPill() {
  const [tokens, setTokens] = useState<number>(0);
  const [cost, setCost] = useState<number>(0);

  const fetchMetrics = async () => {
    try {
      const summary = await getAuditSummary();
      setTokens(summary.total_tokens_consumed || 0);
      setCost(summary.total_cost_usd || 0);
    } catch {
      // Use standard default if not loaded yet
    }
  };

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex items-center space-x-2 bg-gray-900/90 border border-gray-800 rounded-full px-3 py-1 text-xs text-gray-300 shadow-inner">
      <div className="flex items-center space-x-1 text-blue-400">
        <Zap className="h-3.5 w-3.5 fill-blue-400/20" />
        <span className="font-mono font-medium">{tokens.toLocaleString()} tokens</span>
      </div>
      <span className="text-gray-700">|</span>
      <div className="flex items-center space-x-0.5 text-emerald-400">
        <DollarSign className="h-3 w-3" />
        <span className="font-mono font-medium">{formatCurrency(cost).replace('$', '')}</span>
      </div>
    </div>
  );
}
