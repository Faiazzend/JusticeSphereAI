"use client";

import React, { useState } from "react";
import { Search, Filter, AlertCircle, Clock, ShieldCheck, DollarSign, CalendarCheck } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { CalendarExportBtn } from "./calendar-export-btn";
import { ObligationItem } from "@/lib/types";

export function ObligationsTable({
  contractTitle,
  obligations,
}: {
  contractTitle: string;
  obligations: ObligationItem[];
}) {
  const [searchTerm, setSearchTerm] = useState("");
  const [typeFilter, setTypeFilter] = useState("ALL");

  const filteredObligations = obligations.filter((obl) => {
    const matchesSearch =
      obl.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      obl.obligor.toLowerCase().includes(searchTerm.toLowerCase()) ||
      obl.clause_reference.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = typeFilter === "ALL" || obl.obligation_type.toUpperCase() === typeFilter;
    return matchesSearch && matchesType;
  });

  const getTypeIcon = (type: string) => {
    switch (type.toUpperCase()) {
      case "PAYMENT":
        return <DollarSign className="h-4 w-4 text-emerald-400" />;
      case "INSURANCE":
        return <ShieldCheck className="h-4 w-4 text-blue-400" />;
      case "DELIVERY":
        return <CalendarCheck className="h-4 w-4 text-indigo-400" />;
      default:
        return <Clock className="h-4 w-4 text-amber-400" />;
    }
  };

  return (
    <div className="space-y-4">
      {/* Search and Filters */}
      <div className="flex flex-wrap items-center justify-between gap-3 p-4 rounded-xl border border-gray-800 bg-gray-900/60 backdrop-blur-md">
        <div className="flex items-center space-x-2 flex-1 max-w-md">
          <div className="relative w-full">
            <Search className="h-3.5 w-3.5 text-gray-500 absolute left-3 top-3" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search obligations, parties, or citations..."
              className="w-full pl-9 pr-3 py-1.5 rounded-lg bg-gray-950 border border-gray-800 text-xs text-gray-200 placeholder-gray-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="flex items-center space-x-1 bg-gray-950 px-2.5 py-1.5 rounded-lg border border-gray-800 text-xs">
            <Filter className="h-3.5 w-3.5 text-gray-400" />
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="bg-transparent text-gray-300 text-xs focus:outline-none cursor-pointer"
            >
              <option value="ALL">All Categories</option>
              <option value="PAYMENT">Payment</option>
              <option value="INSURANCE">Insurance</option>
              <option value="AUDIT">Audit</option>
              <option value="DELIVERY">Delivery</option>
              <option value="CONFIDENTIALITY">Confidentiality</option>
            </select>
          </div>
        </div>

        <CalendarExportBtn
          contractTitle={contractTitle}
          obligations={obligations}
        />
      </div>

      {/* Structured Table */}
      <div className="overflow-x-auto rounded-2xl border border-white/5 bg-base-200/50 backdrop-blur-md shadow-xl">
        <table className="table table-zebra w-full text-xs">
          <thead className="bg-base-300/80 text-gray-400 uppercase font-mono tracking-wider text-[11px]">
            <tr>
              <th className="py-3.5">Citation</th>
              <th className="py-3.5">Category</th>
              <th className="py-3.5">Obligor</th>
              <th className="py-3.5">Obligation Description</th>
              <th className="py-3.5">Trigger / Due Date</th>
              <th className="py-3.5">Breach Penalty</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5 font-sans">
            {filteredObligations.length === 0 ? (
              <tr>
                <td colSpan={6} className="text-center py-12 text-gray-500">
                  No contractual obligations found matching filter criteria.
                </td>
              </tr>
            ) : (
              filteredObligations.map((obl) => (
                <tr key={obl.id} className="hover:bg-primary/5 transition-colors">
                  <td className="font-mono font-semibold text-primary whitespace-nowrap">
                    {obl.clause_reference}
                  </td>
                  <td className="whitespace-nowrap">
                    <div className="flex items-center space-x-1.5">
                      {getTypeIcon(obl.obligation_type)}
                      <span className="font-medium text-gray-200">{obl.obligation_type}</span>
                    </div>
                  </td>
                  <td className="whitespace-nowrap">
                    <span className="badge badge-neutral font-mono text-[11px]">
                      {obl.obligor}
                    </span>
                  </td>
                  <td className="text-gray-300 max-w-xs leading-relaxed">
                    {obl.description}
                  </td>
                  <td className="text-gray-300 whitespace-nowrap font-mono text-[11px]">
                    <span className="text-warning font-medium">{obl.due_date_or_trigger}</span>
                    <span className="text-gray-500 block text-[10px]">({obl.recurrence})</span>
                  </td>
                  <td className="text-gray-400 max-w-xs leading-relaxed text-[11px]">
                    <div className="flex items-start space-x-1.5">
                      {obl.is_critical && (
                        <span className="badge badge-error badge-xs mt-1 shrink-0">CRITICAL</span>
                      )}
                      <span>{obl.penalty_for_breach}</span>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
