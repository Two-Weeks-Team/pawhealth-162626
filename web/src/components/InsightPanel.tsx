"use client";
import { FC } from "react";
import { CheckCircle } from "lucide-react";

interface AnalysisItem {
  condition: string;
  confidence: number;
  recommendation: string;
}

interface Props {
  analysis: AnalysisItem[];
}

const InsightPanel: FC<Props> = ({ analysis }) => (
  <section className="bg-card p-6 rounded-lg shadow-md mt-6 fade-in">
    <h2 className="text-2xl font-semibold mb-4" style={{ color: "var(--color-accent)"}}>
      AI‑Generated Health Insights
    </h2>
    <ul className="space-y-4">
      {analysis.map((item, idx) => (
        <li key={idx} className="border-b pb-2 last:border-b-0">
          <div className="flex items-center mb-1">
            <CheckCircle className="text-success mr-2" size={20} />
            <span className="font-medium text-foreground">{item.condition}</span>
            <span className="ml-2 text-sm text-muted">({(item.confidence * 100).toFixed(0)}% confidence)</span>
          </div>
          <p className="text-muted">{item.recommendation}</p>
        </li>
      ))}
    </ul>
  </section>
);

export default InsightPanel;
