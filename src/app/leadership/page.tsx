import type { Metadata } from "next";
import { PageHeader } from "@/components/layout/PageHeader";
import { Reveal } from "@/components/ui/Reveal";
import { LeadershipCard } from "@/components/leadership/LeadershipCard";
import { leadership } from "@/data/leadership";

export const metadata: Metadata = {
  title: "Leadership",
  description: "Meet the student leadership team building and running the organization.",
};

export default function LeadershipPage() {
  return (
    <>
      <PageHeader
        eyebrow="Leadership"
        title="Meet the team"
        description="Our organization is student-built and student-led. Leadership focuses on creating opportunities, maintaining the technical infrastructure, and building a welcoming cybersecurity community."
      />

      <section className="py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-6">
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {leadership.map((member, index) => (
              <Reveal key={member.id} delayMs={index * 80}>
                <LeadershipCard member={member} />
              </Reveal>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
