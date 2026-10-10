"use client";

import React from "react";
import { ShieldAlert, AlertTriangle, Info, CheckCircle2 } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export function RiskCategoryCard({
  category,
  severity,
  score,
  rationale,
  mitigation,
}: {
  category: string;
  severity: string;
  score: number;
  rationale: string;
  mitigation: string;
}) {
  const getIcon = (sev: string) => {
    switch (sev) {
      case "CRITICAL":
        return <ShieldAlert className="h-5 w-5 text-red-400" />;
      case "HIGH":
        return <AlertTriangle className="h-5 w-5 text-amber-400" />;
      default:
        return <Info className="h-5 w-5 text-blue-400" />;
    }
  };

  return (
    <div className="p-5 rounded-xl border border-gray-800 bg-gray-900/50 hover:border-gray-700 transition-colors space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2.5">
          {getIcon(severity)}
          <h4 className="text-sm font-semibold text-white">{category}</h4>
        </div>
        <div className="flex items-center space-x-2">
          <Badge
            variant={
              severity === "CRITICAL"
                ? "destructive"
                : severity === "HIGH"
                ? "warning"
                : "secondary"
            }
          >
            {severity}
          </Badge>
          <span className="text-xs font-mono font-bold text-gray-300">
            {score}/100
          </span>
        </div>
      </div>

      <div className="space-y-2 text-xs">
        <div>
          <span className="text-gray-400 font-semibold block mb-0.5">Identified Vulnerability:</span>
          <p className="text-gray-300 leading-relaxed">{rationale}</p>
        </div>

        <div className="p-3 rounded-lg bg-gray-950/70 border border-gray-800/80">
          <span className="text-emerald-400 font-semibold block mb-0.5 flex items-center gap-1">
            <CheckCircle2 className="h-3.5 w-3.5" />
            <span>Playbook Recommended Fix:</span>
          </span>
          <p className="text-gray-300 leading-relaxed">{mitigation}</p>
        </div>
      </div>
    </div>
  );
}
