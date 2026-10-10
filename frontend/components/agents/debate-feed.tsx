"use client";

import React, { useEffect, useState, useRef } from "react";
import { MessageSquare, RefreshCw, Terminal, CheckCircle2 } from "lucide-react";
import { AgentStatusBadge } from "./agent-status-badge";
import { AgentDebateMessage } from "@/lib/types";
import { connectDebateStream } from "@/lib/sse";

export function DebateFeed({
  contractId,
  initialMessages = [],
}: {
  contractId: string;
  initialMessages?: AgentDebateMessage[];
}) {
  const [messages, setMessages] = useState<AgentDebateMessage[]>(initialMessages);
  const [isStreaming, setIsStreaming] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (initialMessages.length > 0) {
      setMessages(initialMessages);
      setIsComplete(true);
      return;
    }

    setIsStreaming(true);
    const unsubscribe = connectDebateStream(
      contractId,
      (newMsg) => {
        setMessages((prev) => [...prev, newMsg]);
        if (scrollRef.current) {
          scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
      },
      () => {
        setIsStreaming(false);
        setIsComplete(true);
      },
      () => {
        setIsStreaming(false);
      }
    );

    return () => {
      unsubscribe();
    };
  }, [contractId, initialMessages]);

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/70 backdrop-blur-md flex flex-col h-[520px]">
      {/* Header bar */}
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-gray-800 bg-gray-950/40 rounded-t-xl">
        <div className="flex items-center space-x-2">
          <Terminal className="h-4 w-4 text-indigo-400" />
          <h4 className="text-xs font-semibold uppercase tracking-wider text-gray-200">
            Multi-Agent Negotiation Debate Transcript
          </h4>
        </div>

        <div className="flex items-center space-x-2">
          {isStreaming ? (
            <div className="flex items-center space-x-1.5 text-xs text-blue-400 font-mono">
              <RefreshCw className="h-3 w-3 animate-spin" />
              <span>Agents Debating...</span>
            </div>
          ) : isComplete ? (
            <div className="flex items-center space-x-1 text-xs text-emerald-400 font-mono">
              <CheckCircle2 className="h-3.5 w-3.5" />
              <span>Consensus Reached</span>
            </div>
          ) : null}
        </div>
      </div>

      {/* Message Feed */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 space-y-3.5 scroll-smooth font-mono text-xs"
      >
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-gray-500 space-y-2">
            <MessageSquare className="h-8 w-8 opacity-40 text-blue-400" />
            <p>Initializing agent deliberation threads...</p>
          </div>
        ) : (
          messages.map((msg, idx) => {
            // Extract model tag if present, e.g. [google/gemini-3.5-flash-lite]
            const modelMatch = msg.content.match(/^\[(.*?)\]\s*/);
            const modelTag = modelMatch ? modelMatch[1] : null;
            const cleanContent = modelTag ? msg.content.replace(/^\[.*?\]\s*/, "") : msg.content;

            return (
              <div
                key={idx}
                className="p-3.5 rounded-lg border border-gray-800/80 bg-gray-950/60 space-y-2 animate-in fade-in-50"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="text-[10px] text-gray-500 font-mono">#{idx + 1}</span>
                    <AgentStatusBadge agentName={msg.agent_name} />
                    {modelTag && (
                      <span className="text-[10px] px-2 py-0.5 rounded-full bg-blue-950/80 text-blue-300 border border-blue-800 font-mono">
                        {modelTag}
                      </span>
                    )}
                  </div>
                  {msg.target_clause && (
                    <span className="text-[10px] text-gray-400 px-2 py-0.5 rounded bg-gray-900 border border-gray-800">
                      Target: {msg.target_clause}
                    </span>
                  )}
                </div>

                <p className="text-gray-200 leading-relaxed text-xs font-sans pl-1">
                  {cleanContent}
                </p>
              </div>
            );
          })
        )}
      </div>

      {/* Footer Info */}
      <div className="px-4 py-2 border-t border-gray-800/60 bg-gray-950/30 text-[11px] text-gray-500 flex justify-between items-center rounded-b-xl">
        <span>Framework: LangGraph Cyclic StateGraph</span>
        <span>Turns: {messages.length}</span>
      </div>
    </div>
  );
}
