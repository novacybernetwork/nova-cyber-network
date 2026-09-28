import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight, MessagesSquare, Radar, Users2 } from "lucide-react";
import { PageHeader } from "@/components/layout/PageHeader";
import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Card } from "@/components/ui/Card";
import { conductRules } from "@/data/codeOfConduct";
import { membershipDefinition, membershipFlexibility } from "@/data/membership";
import { focusAreas } from "@/data/programs";
import { siteConfig } from "@/config/site";

export const metadata: Metadata = {
  title: "About",
  description: siteConfig.whyWeExist,
};

const howItWorks = [
  {
    icon: MessagesSquare,
    title: "A Discord-first community",
    description:
      "Announcements, discussion, and event planning happen in our Discord server — that's the hub for everything.",
  },
  {
    icon: Radar,
    title: "Events posted as they're ready",
    description:
      "CTFs, workshops, and competition-prep sessions are announced with plenty of notice on the Events page and in Discord.",
  },
  {
    icon: Users2,
    title: "Run entirely by students",
    description:
      "Leadership designs challenges, plans events, and maintains this site — all as students, alongside schoolwork.",
  },
];

export default function AboutPage() {
  return (
    <>
      <PageHeader
        eyebrow="About"
        title="An independent, student-led cybersecurity community."
        description={siteConfig.missionShort}
      />

      <section className="border-b border-border py-20 sm:py-28">
        <div className="mx-auto max-w-4xl px-6">
          <Reveal>
            <SectionHeading eyebrow="Our Mission" title="Mission" />
            <p className="mt-6 text-pretty text-lg leading-relaxed text-muted">
              {siteConfig.missionFull}
            </p>
          </Reveal>
        </div>
      </section>

      <section className="border-b border-border py-20 sm:py-28">
        <div className="mx-auto max-w-4xl px-6">
          <Reveal>
            <SectionHeading eyebrow="Why We Exist" title="Closing the access gap" />
            <p className="mt-6 text-pretty text-lg leading-relaxed text-muted">
              {siteConfig.whyWeExist}
            </p>
          </Reveal>
        </div>
      </section>

      <section className="border-b border-border py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-6">
          <Reveal>
            <SectionHeading eyebrow="How It Works" title="How the community runs" />
          </Reveal>
          <div className="mt-12 grid gap-5 sm:grid-cols-3">
            {howItWorks.map((item, index) => (
              <Reveal key={item.title} delayMs={index * 80}>
                <Card className="h-full">
                  <div className="flex h-11 w-11 items-center justify-center rounded-xl border border-border bg-accent-soft text-accent">
                    <item.icon className="h-5 w-5" aria-hidden="true" />
                  </div>
                  <h3 className="mt-4 text-base font-semibold text-foreground">{item.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-muted">{item.description}</p>
                </Card>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="border-b border-border py-20 sm:py-28">
        <div className="mx-auto max-w-4xl px-6">
          <Reveal>
            <SectionHeading eyebrow="Membership" title="Who can join" />
            <p className="mt-6 text-pretty text-lg leading-relaxed text-muted">
              {membershipDefinition}
            </p>
            <p className="mt-4 text-pretty text-base leading-relaxed text-muted">
              {membershipFlexibility}
            </p>
            <Link
              href="/join"
              className="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-accent hover:underline"
            >
              See how to join
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
          </Reveal>
        </div>
      </section>

      <section className="border-b border-border py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-6">
          <Reveal>
            <SectionHeading
              eyebrow="Focus Areas"
              title="Skills our events and workshops touch on"
            />
          </Reveal>
          <Reveal delayMs={80} className="mt-8 flex flex-wrap gap-2.5">
            {focusAreas.map((area) => (
              <span
                key={area}
                className="rounded-full border border-border bg-white/[0.03] px-4 py-2 text-sm font-medium text-muted"
              >
                {area}
              </span>
            ))}
          </Reveal>
        </div>
      </section>

      <section className="py-20 sm:py-28">
        <div className="mx-auto max-w-4xl px-6">
          <Reveal>
            <SectionHeading eyebrow="Code of Conduct" title="How we treat each other" />
            <ul className="mt-6 space-y-2 text-muted">
              {conductRules.slice(0, 3).map((rule) => (
                <li key={rule.title} className="flex gap-2 text-sm leading-relaxed">
                  <span className="mt-2 h-1 w-1 shrink-0 rounded-full bg-accent" aria-hidden="true" />
                  <span>
                    <span className="font-medium text-foreground">{rule.title}:</span>{" "}
                    {rule.body}
                  </span>
                </li>
              ))}
            </ul>
            <Link
              href="/code-of-conduct"
              className="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-accent hover:underline"
            >
              Read the full Code of Conduct
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
          </Reveal>
        </div>
      </section>
    </>
  );
}
