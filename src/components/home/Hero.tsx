import { ArrowRight, CalendarDays } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { siteConfig } from "@/config/site";

export function Hero() {
  return (
    <section className="relative overflow-hidden border-b border-border bg-radial-glow pt-40 pb-24 sm:pt-48 sm:pb-32">
      <div className="bg-cyber-grid pointer-events-none absolute inset-0" aria-hidden="true" />

      <div className="relative mx-auto max-w-4xl px-6 text-center">
        <p
          className="animate-fade-in-up mb-6 inline-flex items-center gap-2 rounded-full border border-border bg-white/[0.03] px-4 py-1.5 font-mono text-xs font-medium tracking-wide text-accent"
          style={{ animationDelay: "0ms" }}
        >
          Independent &middot; Student-Led &middot; Cross-School
        </p>

        <h1
          className="animate-fade-in-up text-balance text-4xl font-semibold tracking-tight text-foreground sm:text-6xl"
          style={{ animationDelay: "80ms" }}
        >
          {siteConfig.headline}
        </h1>

        <p
          className="animate-fade-in-up mx-auto mt-6 max-w-2xl text-pretty text-lg leading-relaxed text-muted sm:text-xl"
          style={{ animationDelay: "160ms" }}
        >
          {siteConfig.subheadline}
        </p>

        <div
          className="animate-fade-in-up mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row"
          style={{ animationDelay: "240ms" }}
        >
          <Button href="/join" variant="primary" icon={<ArrowRight className="h-4 w-4" />}>
            Join the Community
          </Button>
          <Button href="/events" variant="secondary" icon={<CalendarDays className="h-4 w-4" />}>
            View Upcoming Events
          </Button>
        </div>

        <p
          className="animate-fade-in-up mt-8 text-sm text-muted"
          style={{ animationDelay: "320ms" }}
        >
          Built by students. Open to high school students of all experience levels.
        </p>
      </div>
    </section>
  );
}
