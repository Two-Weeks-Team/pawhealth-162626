"use client";
import StatsStrip from "@/components/StatsStrip";
import InsightPanel from "@/components/InsightPanel";
import CollectionPanel from "@/components/CollectionPanel";

export default function Dashboard() {
  return (
    <div className="space-y-8">
      <StatsStrip />
      {/* Placeholder for where insights would appear */}
      <InsightPanel analysis={[]} />
      <CollectionPanel />
    </div>
  );
}
