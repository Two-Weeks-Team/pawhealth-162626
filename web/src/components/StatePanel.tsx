"use client";
import { FC } from "react";
import { Loader2, AlertTriangle } from "lucide-react";

interface Props {
  state: "loading" | "error" | "empty";
  message?: string;
}

const StatePanel: FC<Props> = ({ state, message }) => {
  if (state === "loading") {
    return (
      <div className="flex items-center justify-center py-8">
        <Loader2 className="animate-spin text-primary mr-2" size={24} />
        <span className="text-foreground">Analyzing symptoms…</span>
      </div>
    );
  }
  if (state === "error") {
    return (
      <div className="flex items-center justify-center py-8 text-danger">
        <AlertTriangle className="mr-2" size={24} />
        <span>{message || "Something went wrong. Please try again."}</span>
      </div>
    );
  }
  if (state === "empty") {
    return (
      <div className="text-center py-8 text-muted">
        No insights available. Try logging new symptoms.
      </div>
    );
  }
  return null;
};

export default StatePanel;
