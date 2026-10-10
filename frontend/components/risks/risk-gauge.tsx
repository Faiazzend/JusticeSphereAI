"use client";

import React from "react";

export function RiskGauge({ score }: { score: number }) {
  const safeScore = Math.max(0, Math.min(100, Math.round(score)));
  const radius = 64;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (safeScore / 100) * circumference;

  const getColor = (s: number) => {
    if (s >= 70) return { stroke: "#ef4444", text: "text-red-400", label: "HIGH LEGAL RISK" };
    if (s >= 40) return { stroke: "#f59e0b", text: "text-amber-400", label: "MODERATE RISK" };
    return { stroke: "#10b981", text: "text-emerald-400", label: "LOW RISK (FAVORABLE)" };
  };

  const status = getColor(safeScore);

  return (
    <div className="flex flex-col items-center justify-center p-6 rounded-2xl bg-gray-900/60 border border-gray-800 text-center shadow-xl">
      <div className="relative flex items-center justify-center">
        <svg className="w-40 h-40 transform -rotate-90">
          {/* Background Track */}
          <circle
            cx="80"
            cy="80"
            r={radius}
            stroke="#1f2937"
            strokeWidth="12"
            fill="transparent"
          />
          {/* Progress Stroke */}
          <circle
            cx="80"
            cy="80"
            r={radius}
            stroke={status.stroke}
            strokeWidth="12"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        <div className="absolute flex flex-col items-center">
          <span className={`text-4xl font-extrabold tracking-tight font-mono ${status.text}`}>
            {safeScore}
          </span>
          <span className="text-[11px] uppercase tracking-wider text-gray-500 font-semibold">
            Out of 100
          </span>
        </div>
      </div>

      <div className="mt-3">
        <span className={`text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full bg-gray-950 border border-gray-800 ${status.text}`}>
          {status.label}
        </span>
        <p className="text-[11px] text-gray-400 mt-2 max-w-xs">
          Calculated by multi-agent risk synthesis against the active corporate legal playbook.
        </p>
      </div>
    </div>
  );
}
