import type { Metadata } from "next";
import "./globals.css";
import { Header } from "@/components/layout/header";

export const metadata: Metadata = {
  title: "ContractMind - AI-Native Contract Intelligence Platform",
  description: "Automated contract PDF ingestion, playbook-driven risk scoring, multi-agent redlining, and structured obligations extraction.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark" data-theme="contractmind">
      <body className="min-h-screen bg-[#080c14] text-gray-100 flex flex-col antialiased selection:bg-blue-600 selection:text-white">
        <Header />
        <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {children}
        </main>
        <footer className="footer footer-center p-4 border-t border-white/5 bg-[#05080e] text-xs text-gray-500">
          <aside>
            <p>ContractMind Legal AI Engine &bull; AI Builders Congress 2026 &bull; Multi-Agent FastServer</p>
          </aside>
        </footer>
      </body>
    </html>
  );
}
