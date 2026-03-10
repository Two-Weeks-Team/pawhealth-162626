"use client";
import { FC } from "react";
import { Activity, ClipboardList, ShieldCheck } from "lucide-react";

const stats = [
  { label: "Health Score", value: "87%", icon: ShieldCheck },
  { label: "Active Days", value: "5/7", icon: Activity },
  { label: "Meals Logged", value: "12", icon: ClipboardList }
];

const StatsStrip: FC = () => (
  <section className="flex justify-between bg-card p-4 rounded-lg shadow-md">
    {stats.map((s, i) => (
      <div key={i} className="flex flex-col items-center">
        <s.icon className="text-primary mb-1" />
        <span className="font-medium text-foreground">{s.value}</span>
        <span className="text-sm text-muted">{s.label}</span>
      </div>
    ))}
  </section>
);

export default StatsStrip;
