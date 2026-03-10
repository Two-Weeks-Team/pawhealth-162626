"use client";
import { useEffect, useState } from "react";
import { ClipboardList } from "lucide-react";

interface Insight {
  id: string;
  condition: string;
  created_at: string;
}

export default function CollectionPanel() {
  const [insights, setInsights] = useState<Insight[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Placeholder fetch – in a real app this would call /api/insights
    const fetchRecent = async () => {
      try {
        const res = await fetch("/api/insights");
        if (res.ok) {
          const data = await res.json();
          setInsights(data);
        }
      } catch (e) {
        // ignore for demo
      } finally {
        setLoading(false);
      }
    };
    fetchRecent();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center py-4">
        <ClipboardList className="mr-2 text-primary" />
        <span className="text-muted">Loading recent insights…</span>
      </div>
    );
  }

  if (insights.length === 0) {
    return (
      <div className="py-4 text-muted">
        No saved insights yet. Your AI results will appear here.
      </div>
    );
  }

  return (
    <section className="mt-8">
      <h3 className="text-xl font-semibold mb-4" style={{ color: "var(--color-primary)"}}>
        Recent AI Insights
      </h3>
      <ul className="space-y-2">
        {insights.map((i) => (
          <li key={i.id} className="border-b pb-2 last:border-b-0">
            <span className="font-medium text-foreground">{i.condition}</span>
            <span className="ml-2 text-sm text-muted">{new Date(i.created_at).toLocaleDateString()}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
