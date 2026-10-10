"use client";

import React, { useState } from "react";
import { Info, ShieldAlert } from "lucide-react";

export function RationalePopover({
  rationale,
  severity,
}: {
  rationale: string;
  severity: string;
}) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative inline-block">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-1 text-[11px] text-gray-400 hover:text-blue-400 transition-colors"
      >
        <Info className="h-3.5 w-3.5" />
        <span>Legal Rationale</span>
      </button>

      {isOpen && (
        <>
          <div className="fixed inset-0 z-20" onClick={() => setIsOpen(false)} />
          <div className="absolute right-0 bottom-full mb-2 w-72 p-3.5 rounded-lg border border-gray-700 bg-gray-900 shadow-2xl text-xs z-30 animate-in fade-in-50">
            <div className="flex items-center gap-1.5 text-blue-400 font-semibold mb-1.5">
              <ShieldAlert className="h-3.5 w-3.5" />
              <span>Agent Justification ({severity})</span>
            </div>
            <p className="text-gray-300 leading-relaxed text-[11px]">{rationale}</p>
          </div>
        </>
      )}
    </div>
  );
}
