"use client";

import React from "react";
import { Shield, Scale, PenTool, Bot } from "lucide-react";
import { cn } from "@/lib/utils";

export function AgentStatusBadge({ agentName }: { agentName: string }) {
  if (agentName.toLowerCase().includes("auditor")) {
    return (
      <div className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-blue-950/80 border border-blue-800/80 text-blue-300 text-xs font-semibold shadow-sm">
        <Shield className="h-3.5 w-3.5 text-blue-400" />
        <span>Auditor Agent (Defender)</span>
      </div>
    );
  }

  if (agentName.toLowerCase().includes("opposing")) {
    return (
      <div className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-amber-950/80 border border-amber-800/80 text-amber-300 text-xs font-semibold shadow-sm">
        <Scale className="h-3.5 w-3.5 text-amber-400" />
        <span>Opposing Counsel Agent</span>
      </div>
    );
  }

  if (agentName.toLowerCase().includes("redline") || agentName.toLowerCase().includes("synthesizer")) {
    return (
      <div className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-emerald-950/80 border border-emerald-800/80 text-emerald-300 text-xs font-semibold shadow-sm">
        <PenTool className="h-3.5 w-3.5 text-emerald-400" />
        <span>Redline Synthesizer</span>
      </div>
    );
  }

  return (
    <div className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-gray-800 border border-gray-700 text-gray-300 text-xs font-semibold">
      <Bot className="h-3.5 w-3.5" />
      <span>{agentName}</span>
    </div>
  );
}
