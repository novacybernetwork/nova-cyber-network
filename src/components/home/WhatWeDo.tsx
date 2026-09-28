import { BookOpen, Flag, Presentation, ShieldCheck, Trophy, Users } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { programs, type ProgramIcon } from "@/data/programs";

const iconMap: Record<ProgramIcon, typeof Flag> = {
  flag: Flag,
  presentation: Presentation,
  "shield-check": ShieldCheck,
  trophy: Trophy,
  "book-open": BookOpen,
  users: Users,
};

export function WhatWeDo() {
  return (
    <section className="border-b border-border py-20 sm:py-28">
      <div className="mx-auto max-w-6xl px-6">
        <Reveal>
          <SectionHeading
            eyebrow="What We Do"
            title="Practical cybersecurity, built by students, for students."
            description="Every program is designed to give members real, hands-on experience — not just theory."
          />
        </Reveal>

        <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {programs.map((program, index) => {
            const Icon = iconMap[program.icon];
            return (
              <Reveal key={program.title} delayMs={index * 60}>
                <Card className="h-full">
                  <div className="flex h-11 w-11 items-center justify-center rounded-xl border border-border bg-accent-soft text-accent">
                    <Icon className="h-5 w-5" aria-hidden="true" />
                  </div>
                  <h3 className="mt-4 text-base font-semibold text-foreground">
                    {program.title}
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-muted">
                    {program.description}
                  </p>
                </Card>
              </Reveal>
            );
          })}
        </div>
      </div>
    </section>
  );
}
