"use client";

import React, { useState } from "react";
import { Calendar, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ObligationItem } from "@/lib/types";

export function CalendarExportBtn({
  contractTitle,
  obligations,
}: {
  contractTitle: string;
  obligations: ObligationItem[];
}) {
  const [downloaded, setDownloaded] = useState(false);

  const exportICS = () => {
    // Generate RFC 5545 iCalendar format file
    let icsContent = [
      "BEGIN:VCALENDAR",
      "VERSION:2.0",
      "PRODID:-//ContractMind Legal AI//Contract Obligations Calendar//EN",
      "CALSCALE:GREGORIAN",
      "METHOD:PUBLISH",
    ];

    const now = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";

    obligations.forEach((obl, idx) => {
      // Create event scheduled 30 days in future or today
      const eventDate = new Date();
      eventDate.setDate(eventDate.getDate() + 30 * (idx + 1));
      const dtString = eventDate.toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";

      icsContent.push(
        "BEGIN:VEVENT",
        `UID:contractmind-${obl.id}@legal.ai`,
        `DTSTAMP:${now}`,
        `DTSTART:${dtString}`,
        `SUMMARY:[${obl.obligation_type}] ${obl.description.substring(0, 50)}...`,
        `DESCRIPTION:Contract: ${contractTitle}\\nObligor: ${obl.obligor}\\nTrigger: ${obl.due_date_or_trigger}\\nPenalty: ${obl.penalty_for_breach}`,
        "STATUS:CONFIRMED",
        "END:VEVENT"
      );
    });

    icsContent.push("END:VCALENDAR");

    const blob = new Blob([icsContent.join("\r\n")], { type: "text/calendar;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${contractTitle.replace(/\s+/g, "_")}_obligations.ics`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    setDownloaded(true);
    setTimeout(() => setDownloaded(false), 3000);
  };

  return (
    <Button
      variant="outline"
      size="sm"
      onClick={exportICS}
      className="flex items-center gap-1.5 h-9 bg-gray-900 border-gray-700 hover:bg-gray-800 text-xs"
    >
      {downloaded ? (
        <>
          <Check className="h-3.5 w-3.5 text-emerald-400" />
          <span className="text-emerald-400">Synced to iCal!</span>
        </>
      ) : (
        <>
          <Calendar className="h-3.5 w-3.5 text-indigo-400" />
          <span>Sync to Calendar (.ICS)</span>
        </>
      )}
    </Button>
  );
}
