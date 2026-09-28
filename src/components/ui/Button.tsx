import Link from "next/link";
import type { ReactNode } from "react";

type Variant = "primary" | "secondary" | "ghost" | "disabled";

const base =
  "inline-flex items-center justify-center gap-2 rounded-full px-6 py-3 text-sm font-semibold transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60 focus-visible:ring-offset-2 focus-visible:ring-offset-background";

const variants: Record<Variant, string> = {
  primary:
    "bg-accent text-background hover:bg-accent/90 hover:shadow-[0_0_0_1px_rgba(56,189,248,0.4),0_8px_30px_-8px_rgba(56,189,248,0.5)] active:scale-[0.98]",
  secondary:
    "border border-border bg-white/[0.03] text-foreground hover:border-accent/40 hover:bg-white/[0.06] active:scale-[0.98]",
  ghost: "text-foreground/80 hover:text-accent",
  disabled: "cursor-not-allowed border border-border bg-white/[0.02] text-muted",
};

interface CommonProps {
  variant?: Variant;
  icon?: ReactNode;
  className?: string;
  children: ReactNode;
}

interface LinkButtonProps extends CommonProps {
  href: string;
  target?: string;
  rel?: string;
}

interface ElementButtonProps extends CommonProps {
  href?: undefined;
  type?: "button" | "submit";
  onClick?: () => void;
  disabled?: boolean;
}

export function Button(props: LinkButtonProps | ElementButtonProps) {
  const { variant = "primary", icon, className = "", children } = props;
  const classes = `${base} ${variants[variant]} ${className}`;

  if ("href" in props && props.href) {
    // next/link requires a real relative or absolute URL. Config values are
    // sometimes left as unfilled "[PLACEHOLDER]" tokens, which aren't valid
    // hrefs — fall back to a plain anchor so the page still renders instead
    // of throwing at runtime.
    const isInternal = props.href.startsWith("/");

    if (isInternal) {
      return (
        <Link href={props.href} target={props.target} rel={props.rel} className={classes}>
          {children}
          {icon}
        </Link>
      );
    }

    return (
      <a href={props.href} target={props.target} rel={props.rel} className={classes}>
        {children}
        {icon}
      </a>
    );
  }

  const { type = "button", onClick, disabled } = props as ElementButtonProps;

  return (
    <button type={type} onClick={onClick} disabled={disabled} className={classes}>
      {children}
      {icon}
    </button>
  );
}
