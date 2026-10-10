"use client";

import React, { useState } from "react";
import { Download, FileText, Code2, Check, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { getExportDocxUrl } from "@/lib/api";

export function ExportMenu({
  contractId,
  contractTitle,
  obligationsData,
  redlinesData,
}: {
  contractId: string;
  contractTitle: string;
  obligationsData: any;
  redlinesData: any;
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [downloaded, setDownloaded] = useState<string | null>(null);

  const downloadJSON = (data: any, filename: string) => {
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    setDownloaded(filename);
    setTimeout(() => setDownloaded(null), 2500);
  };

  return (
    <div className="relative inline-block text-left">
      <Button
        variant="outline"
        size="sm"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-1.5 h-9 bg-gray-900 border-gray-700 hover:bg-gray-800 text-xs"
      >
        <Download className="h-3.5 w-3.5 text-blue-400" />
        <span>Export Deliverables</span>
        <ChevronDown className="h-3 w-3 ml-0.5 text-gray-400" />
      </Button>

      {isOpen && (
        <>
          <div className="fixed inset-0 z-20" onClick={() => setIsOpen(false)} />
          <div className="absolute right-0 mt-2 w-64 rounded-xl border border-gray-800 bg-gray-900 p-1.5 shadow-2xl z-30 animate-in fade-in-50 text-xs">
            {/* Export DOCX with Track Changes */}
            <a
              href={getExportDocxUrl(contractId)}
              download
              onClick={() => setIsOpen(false)}
              className="flex items-center space-x-2.5 px-3 py-2.5 rounded-lg hover:bg-gray-800 transition-colors text-gray-200"
            >
              <FileText className="h-4 w-4 text-blue-400" />
              <div>
                <p className="font-semibold text-white">Word (.DOCX) Redline</p>
                <p className="text-[11px] text-gray-400">Track Changes markup</p>
              </div>
            </a>

            {/* Export Obligations JSON */}
            <button
              onClick={() => {
                downloadJSON(
                  obligationsData,
                  `${contractTitle.replace(/\s+/g, "_")}_obligations.json`
                );
                setIsOpen(false);
              }}
              className="w-full flex items-center space-x-2.5 px-3 py-2.5 rounded-lg hover:bg-gray-800 transition-colors text-left text-gray-200"
            >
              <Code2 className="h-4 w-4 text-emerald-400" />
              <div>
                <p className="font-semibold text-white">Obligations JSON</p>
                <p className="text-[11px] text-gray-400">Strict structured schema</p>
              </div>
            </button>

            {/* Export Full Analysis JSON */}
            <button
              onClick={() => {
                downloadJSON(
                  { redlines: redlinesData, obligations: obligationsData },
                  `${contractTitle.replace(/\s+/g, "_")}_full_analysis.json`
                );
                setIsOpen(false);
              }}
              className="w-full flex items-center space-x-2.5 px-3 py-2.5 rounded-lg hover:bg-gray-800 transition-colors text-left text-gray-200"
            >
              <Code2 className="h-4 w-4 text-indigo-400" />
              <div>
                <p className="font-semibold text-white">Full Review JSON</p>
                <p className="text-[11px] text-gray-400">Risks, debate, & diff tokens</p>
              </div>
            </button>
          </div>
        </>
      )}

      {downloaded && (
        <div className="fixed bottom-6 right-6 bg-emerald-950 border border-emerald-800 text-emerald-200 px-4 py-2.5 rounded-lg text-xs shadow-2xl flex items-center gap-2 z-50 animate-in slide-in-from-bottom-5">
          <Check className="h-4 w-4 text-emerald-400" />
          <span>Downloaded {downloaded}</span>
        </div>
      )}
    </div>
  );
}
