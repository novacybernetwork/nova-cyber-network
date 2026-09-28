import { Reveal } from "@/components/ui/Reveal";
import { stats, statsNote } from "@/data/stats";

export function StatsSection() {
  return (
    <section className="border-b border-border py-16 sm:py-20" aria-label="Organization statistics">
      <div className="mx-auto max-w-6xl px-6">
        <div className="grid grid-cols-2 gap-8 sm:grid-cols-4">
          {stats.map((stat, index) => (
            <Reveal key={stat.label} delayMs={index * 80} className="text-center">
              <p className="font-mono text-3xl font-semibold text-foreground sm:text-4xl">
                {stat.value}
              </p>
              <p className="mt-2 text-sm text-muted">{stat.label}</p>
            </Reveal>
          ))}
        </div>
        <p className="mt-10 text-center text-sm text-muted/80">{statsNote}</p>
      </div>
    </section>
  );
}
