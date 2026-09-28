import { Reveal } from "@/components/ui/Reveal";
import { siteConfig } from "@/config/site";
import { focusAreas } from "@/data/programs";

export function MissionSection() {
  return (
    <section className="relative overflow-hidden border-b border-border py-20 sm:py-28">
      <div className="bg-cyber-grid pointer-events-none absolute inset-0" aria-hidden="true" />
      <div className="relative mx-auto max-w-4xl px-6 text-center">
        <Reveal>
          <p className="font-mono text-xs font-medium tracking-[0.2em] text-accent uppercase">
            Our Mission
          </p>
          <p className="mt-4 text-balance text-2xl leading-relaxed font-medium text-foreground sm:text-3xl">
            {siteConfig.missionFull}
          </p>
        </Reveal>

        <Reveal delayMs={100} className="mt-10 flex flex-wrap justify-center gap-2">
          {focusAreas.map((area) => (
            <span
              key={area}
              className="rounded-full border border-border bg-white/[0.03] px-3.5 py-1.5 text-xs font-medium text-muted"
            >
              {area}
            </span>
          ))}
        </Reveal>
      </div>
    </section>
  );
}
