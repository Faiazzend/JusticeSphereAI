"use client";

import React, { useState } from "react";
import { Check, X, Undo, Sparkles } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { RationalePopover } from "./rationale-popover";
import { RedlineChange } from "@/lib/types";
import { updateRedlineDecision } from "@/lib/api";

export function ClauseCard({
  contractId,
  redline,
  viewMode,
}: {
  contractId: string;
  redline: RedlineChange;
  viewMode: "unified" | "split";
}) {
  const [decision, setDecision] = useState<boolean | null>(redline.accepted);
  const [loading, setLoading] = useState(false);

  const handleDecision = async (accepted: boolean | null) => {
    try {
      setLoading(true);
      await updateRedlineDecision(contractId, redline.id, accepted);
      setDecision(accepted);
    } catch (err) {
      console.error("Failed to update decision", err);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityBadge = (sev: string) => {
    switch (sev) {
      case "CRITICAL":
        return <Badge variant="destructive">CRITICAL EXPOSURE</Badge>;
      case "HIGH":
        return <Badge variant="warning">HIGH RISK</Badge>;
      case "MEDIUM":
        return <Badge variant="secondary">MODERATE</Badge>;
      default:
        return <Badge variant="outline">LOW RISK</Badge>;
    }
  };

  return (
    <div
      className={`rounded-xl border transition-all ${
        decision === true
          ? "border-emerald-800/80 bg-emerald-950/10"
          : decision === false
          ? "border-red-800/50 bg-red-950/10 opacity-75"
          : "border-gray-800 bg-gray-900/60"
      }`}
    >
      {/* Header bar */}
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-gray-800/70 bg-gray-950/30 rounded-t-xl">
        <div className="flex items-center space-x-3">
          <span className="text-xs font-mono font-bold text-gray-200">
            Section {redline.section_number}
          </span>
          {getSeverityBadge(redline.risk_severity)}
          <span className="text-[11px] font-mono text-gray-400">
            [{redline.diff_type}]
          </span>
        </div>

        <div className="flex items-center space-x-2">
          <RationalePopover
            rationale={redline.legal_rationale}
            severity={redline.risk_severity}
          />
        </div>
      </div>

      {/* Main Content Body */}
      <div className="p-5">
        {viewMode === "split" ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Original Box */}
            <div className="p-3.5 rounded-lg bg-gray-950/60 border border-gray-800 text-xs">
              <span className="text-[11px] font-bold text-gray-400 uppercase tracking-wider block mb-2">
                Original Contract Text
              </span>
              <p className="text-gray-300 leading-relaxed font-mono whitespace-pre-wrap">
                {redline.original_text}
              </p>
            </div>

            {/* Suggested Replacement */}
            <div className="p-3.5 rounded-lg bg-emerald-950/20 border border-emerald-900/40 text-xs">
              <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-wider block mb-2 flex items-center gap-1">
                <Sparkles className="h-3 w-3" />
                <span>AI Suggested Redline</span>
              </span>
              <p className="text-emerald-200 leading-relaxed font-mono whitespace-pre-wrap">
                {redline.suggested_text}
              </p>
            </div>
          </div>
        ) : (
          /* Unified Track Changes View */
          <div className="p-4 rounded-lg bg-gray-950/60 border border-gray-800 text-xs leading-relaxed font-mono">
            {redline.diff_tokens && redline.diff_tokens.length > 0 ? (
              <div>
                {redline.diff_tokens.map((tok, i) => {
                  if (tok.type === "delete") {
                    return (
                      <span key={i} className="diff-del mr-1">
                        {tok.text}{" "}
                      </span>
                    );
                  }
                  if (tok.type === "insert") {
                    return (
                      <span key={i} className="diff-ins mr-1">
                        {tok.text}{" "}
                      </span>
                    );
                  }
                  return (
                    <span key={i} className="text-gray-300 mr-1">
                      {tok.text}{" "}
                    </span>
                  );
                })}
              </div>
            ) : (
              <div>
                <p className="text-red-400/80 line-through mb-2">
                  {redline.original_text}
                </p>
                <p className="text-emerald-400">
                  {redline.suggested_text}
                </p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Action Footer */}
      <div className="flex items-center justify-between px-5 py-3 border-t border-gray-800/60 bg-gray-950/20 rounded-b-xl">
        <div className="text-[11px] text-gray-400">
          {decision === true && (
            <span className="text-emerald-400 font-semibold flex items-center gap-1">
              <Check className="h-3.5 w-3.5" /> Change Accepted
            </span>
          )}
          {decision === false && (
            <span className="text-red-400 font-semibold flex items-center gap-1">
              <X className="h-3.5 w-3.5" /> Change Rejected
            </span>
          )}
          {decision === null && <span>Awaiting reviewer approval</span>}
        </div>

        <div className="flex items-center space-x-2">
          {decision !== null ? (
            <Button
              variant="outline"
              size="sm"
              disabled={loading}
              onClick={() => handleDecision(null)}
              className="text-xs h-7 text-gray-400 hover:text-white"
            >
              <Undo className="h-3 w-3 mr-1" /> Reset
            </Button>
          ) : (
            <>
              <Button
                variant="outline"
                size="sm"
                disabled={loading}
                onClick={() => handleDecision(false)}
                className="text-xs h-7 text-red-400 border-red-900/60 hover:bg-red-950/40"
              >
                <X className="h-3 w-3 mr-1" /> Reject
              </Button>
              <Button
                size="sm"
                disabled={loading}
                onClick={() => handleDecision(true)}
                className="text-xs h-7 bg-emerald-600 hover:bg-emerald-500 text-white"
              >
                <Check className="h-3 w-3 mr-1" /> Accept Redline
              </Button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
