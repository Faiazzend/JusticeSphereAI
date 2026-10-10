"use client";

import React, { useState } from "react";
import { Columns2, AlignLeft, Filter, Sparkles } from "lucide-react";
import { ClauseCard } from "./clause-card";
import { ExportMenu } from "./export-menu";
import { RedlineChange, ObligationItem } from "@/lib/types";

export function RedlineViewer({
  contractId,
  contractTitle,
  redlines,
  obligations,
}: {
  contractId: string;
  contractTitle: string;
  redlines: RedlineChange[];
  obligations: ObligationItem[];
}) {
  const [viewMode, setViewMode] = useState<"unified" | "split">("unified");
  const [filterSeverity, setFilterSeverity] = useState<string>("ALL");

  const filteredRedlines = redlines.filter((rl) => {
    if (filterSeverity === "ALL") return true;
    return rl.risk_severity === filterSeverity;
  });

  const acceptedCount = redlines.filter((rl) => rl.accepted === true).length;
  const rejectedCount = redlines.filter((rl) => rl.accepted === false).length;
  const pendingCount = redlines.filter((rl) => rl.accepted === null).length;

  return (
    <div className="space-y-4">
      {/* Action and Filter Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-3 p-4 rounded-xl border border-gray-800 bg-gray-900/60 backdrop-blur-md">
        <div className="flex items-center space-x-2">
          {/* View Mode Toggle */}
          <div className="flex items-center rounded-lg bg-gray-950 p-1 border border-gray-800">
            <button
              onClick={() => setViewMode("unified")}
              className={`flex items-center space-x-1.5 px-3 py-1 rounded-md text-xs font-medium transition-colors ${
                viewMode === "unified"
                  ? "bg-gray-800 text-white shadow-sm"
                  : "text-gray-400 hover:text-gray-200"
              }`}
            >
              <AlignLeft className="h-3.5 w-3.5" />
              <span>Track Changes</span>
            </button>
            <button
              onClick={() => setViewMode("split")}
              className={`flex items-center space-x-1.5 px-3 py-1 rounded-md text-xs font-medium transition-colors ${
                viewMode === "split"
                  ? "bg-gray-800 text-white shadow-sm"
                  : "text-gray-400 hover:text-gray-200"
              }`}
            >
              <Columns2 className="h-3.5 w-3.5" />
              <span>Side-by-Side</span>
            </button>
          </div>

          {/* Severity Filter */}
          <div className="flex items-center space-x-1 bg-gray-950 px-2.5 py-1 rounded-lg border border-gray-800 text-xs">
            <Filter className="h-3.5 w-3.5 text-gray-400" />
            <select
              value={filterSeverity}
              onChange={(e) => setFilterSeverity(e.target.value)}
              className="bg-transparent text-gray-300 text-xs focus:outline-none cursor-pointer"
            >
              <option value="ALL">All Severities ({redlines.length})</option>
              <option value="CRITICAL">Critical Only</option>
              <option value="HIGH">High Risk</option>
              <option value="MEDIUM">Moderate</option>
              <option value="LOW">Low Risk</option>
            </select>
          </div>
        </div>

        {/* Counter and Export Menu */}
        <div className="flex items-center space-x-4">
          <div className="hidden sm:flex items-center space-x-2 text-xs font-mono">
            <span className="text-emerald-400 font-semibold">{acceptedCount} Accepted</span>
            <span className="text-gray-600">/</span>
            <span className="text-red-400 font-semibold">{rejectedCount} Rejected</span>
            <span className="text-gray-600">/</span>
            <span className="text-gray-400 font-semibold">{pendingCount} Pending</span>
          </div>

          <ExportMenu
            contractId={contractId}
            contractTitle={contractTitle}
            obligationsData={obligations}
            redlinesData={redlines}
          />
        </div>
      </div>

      {/* Redline Cards List */}
      {filteredRedlines.length === 0 ? (
        <div className="p-12 text-center border border-dashed border-gray-800 rounded-xl bg-gray-950/40">
          <Sparkles className="h-8 w-8 text-blue-400 mx-auto mb-2 opacity-60" />
          <p className="text-sm text-gray-300 font-semibold">No redlines match the selected filter</p>
          <p className="text-xs text-gray-500 mt-1">Select "All Severities" to review full consensus modifications.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredRedlines.map((rl) => (
            <ClauseCard
              key={rl.id}
              contractId={contractId}
              redline={rl}
              viewMode={viewMode}
            />
          ))}
        </div>
      )}
    </div>
  );
}
