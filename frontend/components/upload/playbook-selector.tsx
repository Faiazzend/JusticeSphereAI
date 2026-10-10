"use client";

import React from "react";
import { BookOpen, ShieldAlert, Rocket } from "lucide-react";
import { cn } from "@/lib/utils";

export interface PlaybookOption {
  id: string;
  name: string;
  description: string;
  icon: React.ReactNode;
  riskTolerance: "Low" | "Medium" | "High";
}

const PLAYBOOK_OPTIONS: PlaybookOption[] = [
  {
    id: "Standard Corporate Playbook",
    name: "Standard Corporate",
    description: "Enterprise grade. Demands mutual indemnification, 1x liability caps, and preserves Background IP.",
    icon: <BookOpen className="h-4 w-4 text-blue-400" />,
    riskTolerance: "Low",
  },
  {
    id: "Aggressive Startup Playbook",
    name: "Aggressive Startup",
    description: "High speed closure. Relaxed liability caps ($250k) and flexible IP licenses to close deals fast.",
    icon: <Rocket className="h-4 w-4 text-amber-400" />,
    riskTolerance: "High",
  },
  {
    id: "Vendor Friendly Playbook",
    name: "Vendor Friendly",
    description: "Maximizes vendor protections, shields proprietary source code, and strictly enforces payment cure periods.",
    icon: <ShieldAlert className="h-4 w-4 text-emerald-400" />,
    riskTolerance: "Medium",
  },
];

export function PlaybookSelector({
  selected,
  onSelect,
}: {
  selected: string;
  onSelect: (name: string) => void;
}) {
  return (
    <div className="space-y-1.5">
      <label className="text-xs font-semibold uppercase tracking-wider text-gray-400">
        Review Playbook Profile
      </label>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
        {PLAYBOOK_OPTIONS.map((pb) => {
          const isSelected = selected === pb.id;
          return (
            <div
              key={pb.id}
              onClick={() => onSelect(pb.id)}
              className={cn(
                "p-2.5 rounded-lg border cursor-pointer transition-all flex flex-col justify-between text-left",
                isSelected
                  ? "border-blue-500 bg-blue-950/25 ring-1 ring-blue-500/30"
                  : "border-gray-800 bg-gray-900/40 hover:border-gray-700 hover:bg-gray-900/60"
              )}
            >
              <div>
                <div className="flex items-center justify-between mb-1">
                  <div className="flex items-center space-x-1.5">
                    {pb.icon}
                    <span className="text-xs font-semibold text-gray-200">{pb.name}</span>
                  </div>
                  <span
                    className={cn(
                      "text-[9px] px-1.5 py-0.2 rounded font-medium",
                      pb.riskTolerance === "Low"
                        ? "bg-blue-900/50 text-blue-300"
                        : pb.riskTolerance === "Medium"
                        ? "bg-emerald-900/50 text-emerald-300"
                        : "bg-amber-900/50 text-amber-300"
                    )}
                  >
                    {pb.riskTolerance} Risk
                  </span>
                </div>
                <p className="text-[11px] text-gray-400 leading-snug line-clamp-1">
                  {pb.description}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
