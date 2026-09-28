import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { LeadershipCard } from "@/components/leadership/LeadershipCard";
import { leadership } from "@/data/leadership";

export function LeadershipPreview() {
  return (
    <section className="border-b border-border py-20 sm:py-28">
      <div className="mx-auto max-w-6xl px-6">
        <div className="flex flex-wrap items-end justify-between gap-6">
          <Reveal>
            <SectionHeading eyebrow="Leadership" title="Student-built, student-led." />
          </Reveal>
          <Reveal delayMs={80}>
            <Button href="/leadership" variant="ghost" icon={<ArrowRight className="h-4 w-4" />}>
              Meet the team
            </Button>
          </Reveal>
        </div>

        <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {leadership.map((member, index) => (
            <Reveal key={member.id} delayMs={index * 80}>
              <LeadershipCard member={member} />
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
