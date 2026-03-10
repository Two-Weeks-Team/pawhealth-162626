"use client";

import { useState } from "react";
import Hero from "@/components/Hero";
import StatsStrip from "@/components/StatsStrip";
import InsightPanel from "@/components/InsightPanel";
import StatePanel from "@/components/StatePanel";
import CollectionPanel from "@/components/CollectionPanel";
import { analyzeSymptoms, getPet } from "@/lib/api";

interface AnalysisResult {
  condition: string;
  confidence: number;
  recommendation: string;
}

export default function HomePage() {
  const [analysis, setAnalysis] = useState<AnalysisResult[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const demoPetId = "demo-pet-id";

  const startCheck = async () => {
    setLoading(true);
    setError(null);
    try {
      // fetch pet profile (demo only, ignore result)
      await getPet(demoPetId);
      // dummy symptom payload
      const payload = [
        { symptom: "coughing", severity: 3, date: new Date().toISOString() },
        { symptom: "lethargy", severity: 2, date: new Date().toISOString() }
      ];
      const resp = await analyzeSymptoms(demoPetId, payload);
      setAnalysis(resp.analysis);
    } catch (e: any) {
      setError(e.message || "Unexpected error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="max-w-6xl mx-auto p-4 space-y-8">
      <Hero onStart={startCheck} />
      <StatsStrip />
      {loading && <StatePanel state="loading" />}
      {error && <StatePanel state="error" message={error} />}
      {analysis && analysis.length > 0 && <InsightPanel analysis={analysis} />}
      {analysis && analysis.length === 0 && <StatePanel state="empty" />}
      <CollectionPanel />
    </main>
  );
}
