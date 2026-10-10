"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Scale, Activity, ShieldCheck, Cpu, Sparkles, BookOpen } from "lucide-react";
import { TokenCounterPill } from "./token-counter-pill";
import { Badge } from "@/components/ui/badge";
import { getMCPTools, getLLMConfig } from "@/lib/api";

export function Header() {
  const pathname = usePathname();
  const [mcpActive, setMcpActive] = useState(true);
  const [activeEngine, setActiveEngine] = useState("Gemini 3.5");

  useEffect(() => {
    getMCPTools().then(res => {
      setMcpActive(Boolean(res.tools && res.tools.length > 0));
    }).catch(() => setMcpActive(true));

    getLLMConfig().then(cfg => {
      if (cfg.gemini_configured) setActiveEngine("Gemini 3.5");
      else if (cfg.ollama_available) setActiveEngine("Ollama Local");
      else if (cfg.openai_configured) setActiveEngine("GPT-4o");
    }).catch(() => {});
  }, []);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-white/5 bg-[#080c14]/80 backdrop-blur-xl">
      <div className="flex h-16 items-center justify-between px-4 sm:px-8 max-w-7xl mx-auto">
        {/* Brand & Identity */}
        <div className="flex items-center space-x-6">
          <Link href="/" className="flex items-center space-x-3 group">
            <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-blue-500/25 ring-1 ring-white/20 group-hover:scale-105 transition-all duration-200">
              <Scale className="h-5 w-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="text-base font-bold tracking-tight text-white group-hover:text-blue-300 transition-colors">
                  ContractMind
                </span>
                <span className="text-[10px] font-semibold px-1.5 py-0.2 rounded bg-blue-500/15 text-blue-400 border border-blue-500/30 font-mono">
                  v1.5
                </span>
              </div>
              <p className="text-[10px] text-gray-400 -mt-0.5 tracking-wide">Autonomous Legal Redline AI</p>
            </div>
          </Link>

          {/* Quick Nav Links */}
          <nav className="hidden md:flex items-center space-x-1 pl-4 border-l border-gray-800/80 text-xs">
            <Link
              href="/"
              className={`px-3 py-1.5 rounded-lg transition-colors font-medium ${
                pathname === "/" 
                  ? "bg-white/10 text-white" 
                  : "text-gray-400 hover:text-gray-200 hover:bg-white/5"
              }`}
            >
              Analysis Studio
            </Link>
            <Link
              href="/audit"
              className={`px-3 py-1.5 rounded-lg transition-colors font-medium flex items-center gap-1.5 ${
                pathname === "/audit" 
                  ? "bg-white/10 text-white" 
                  : "text-gray-400 hover:text-gray-200 hover:bg-white/5"
              }`}
            >
              <Activity className="h-3.5 w-3.5 text-blue-400" />
              Telemetry & Audits
            </Link>
          </nav>
        </div>

        {/* Status Indicators & Telemetry Pill */}
        <div className="flex items-center space-x-3">
          {/* Active Model Indicator */}
          <div className="hidden lg:flex items-center space-x-2 text-xs bg-gray-900/60 border border-gray-800 rounded-full px-3 py-1">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-gray-400">Engine:</span>
            <span className="font-semibold text-gray-200 font-mono">{activeEngine}</span>
          </div>

          <TokenCounterPill />
        </div>
      </div>
    </header>
  );
}
