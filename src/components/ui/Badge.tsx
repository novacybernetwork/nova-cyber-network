import type { ReactNode } from "react";

interface BadgeProps {
  children: ReactNode;
  className?: string;
}

export function Badge({ children, className = "" }: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full border border-border bg-white/[0.03] px-3 py-1 text-xs font-medium text-muted ${className}`}
    >
      {children}
    </span>
  );
}
