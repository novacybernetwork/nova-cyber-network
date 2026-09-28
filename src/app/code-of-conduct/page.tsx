import type { Metadata } from "next";
import { PageHeader } from "@/components/layout/PageHeader";
import { Reveal } from "@/components/ui/Reveal";
import { Card } from "@/components/ui/Card";
import { conductAgreement, conductRules } from "@/data/codeOfConduct";

export const metadata: Metadata = {
  title: "Code of Conduct",
  description: "The expectations every participant agrees to by joining the community.",
};

export default function CodeOfConductPage() {
  return (
    <>
      <PageHeader
        eyebrow="Code of Conduct"
        title="How we expect each other to act"
        description={conductAgreement}
      />

      <section className="py-20 sm:py-28">
        <div className="mx-auto max-w-3xl px-6">
          <ol className="space-y-5">
            {conductRules.map((rule, index) => (
              <Reveal key={rule.title} delayMs={index * 50} as="li">
                <Card hover={false} className="flex gap-4">
                  <span className="font-mono text-sm text-accent">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <div>
                    <h2 className="text-base font-semibold text-foreground">{rule.title}</h2>
                    <p className="mt-1.5 text-sm leading-relaxed text-muted">{rule.body}</p>
                  </div>
                </Card>
              </Reveal>
            ))}
          </ol>
        </div>
      </section>
    </>
  );
}
