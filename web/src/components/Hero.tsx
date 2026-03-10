"use client";
import { FC } from "react";
import { HeartPulse } from "lucide-react";
import clsx from "clsx";

interface HeroProps {
  onStart: () => void;
}

const Hero: FC<HeroProps> = ({ onStart }) => (
  <section className="text-center py-12 fade-in">
    <h1 className="text-5xl font-bold mb-4" style={{ color: "var(--color-primary)"}}>
      PawHealth
    </h1>
    <p className="text-xl mb-6 text-foreground">Track. Analyze. Care.</p>
    <button className={clsx("btn-primary", "flex", "items-center", "gap-2", "mx-auto")}
            onClick={onStart}>
      <HeartPulse size={20} /> Start Symptom Check
    </button>
    <div className="mt-8 text-sm text-muted">
      <span>Trusted by veterinarians • AI accuracy: 92%</span>
    </div>
  </section>
);

export default Hero;
