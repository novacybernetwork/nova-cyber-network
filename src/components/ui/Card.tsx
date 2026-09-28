import type { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
}

export function Card({ children, className = "", hover = true }: CardProps) {
  return (
    <div
      className={`group relative rounded-2xl border border-border bg-white/[0.02] p-6 transition-all duration-300 ${
        hover ? "hover:-translate-y-1 hover:border-accent/30 hover:bg-white/[0.04]" : ""
      } ${className}`}
    >
      {children}
    </div>
  );
}
