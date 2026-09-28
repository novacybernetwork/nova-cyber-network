import type { Metadata } from "next";
import { ClipboardList, MessageCircle, Radar, Rocket } from "lucide-react";
import { PageHeader } from "@/components/layout/PageHeader";
import { Reveal } from "@/components/ui/Reveal";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { joinSteps } from "@/data/membership";
import { siteConfig } from "@/config/site";

export const metadata: Metadata = {
  title: "Join",
  description:
    "Whether you're new to cybersecurity or already competing in CyberPatriot, NCL, or CTFs, you're welcome to join.",
};

const stepIcons = [ClipboardList, MessageCircle, Radar, Rocket];

export default function JoinPage() {
  return (
    <>
      <PageHeader
        eyebrow="Join"
        title="Join the Community"
        description="Whether you're completely new to cybersecurity or already competing in CyberPatriot, NCL, or CTFs, you're welcome to join."
      />

      <section className="border-b border-border py-20 sm:py-28">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <Reveal className="flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
            <Button href={siteConfig.links.joinForm} variant="primary" target="_blank" rel="noreferrer noopener">
              Join Interest Form
            </Button>
            {siteConfig.links.communityChat ? (
              <Button
                href={siteConfig.links.communityChat}
                variant="secondary"
                target="_blank"
                rel="noreferrer noopener"
              >
                Join the Chat
              </Button>
            ) : (
              <Button variant="disabled" disabled>
                Community Chat Coming Soon
              </Button>
            )}
          </Reveal>
          <Reveal delayMs={100}>
            <p className="mt-6 text-sm text-muted">
              Questions first? Reach out at{" "}
              <a href={`mailto:${siteConfig.email}`} className="font-medium text-accent hover:underline">
                {siteConfig.email}
              </a>
            </p>
          </Reveal>
        </div>
      </section>

      <section className="py-20 sm:py-28">
        <div className="mx-auto max-w-4xl px-6">
          <Reveal>
            <SectionHeading eyebrow="The Process" title="How it works" align="center" />
          </Reveal>

          <div className="mt-12 grid gap-5 sm:grid-cols-2">
            {joinSteps.map((step, index) => {
              const Icon = stepIcons[index];
              return (
                <Reveal key={step.title} delayMs={index * 80}>
                  <Card className="flex h-full items-start gap-4">
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-accent/30 bg-accent-soft font-mono text-sm font-semibold text-accent">
                      {index + 1}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <Icon className="h-4 w-4 text-accent" aria-hidden="true" />
                        <h3 className="text-sm font-semibold text-foreground">{step.title}</h3>
                      </div>
                      <p className="mt-1.5 text-sm leading-relaxed text-muted">
                        {step.description}
                      </p>
                    </div>
                  </Card>
                </Reveal>
              );
            })}
          </div>
        </div>
      </section>
    </>
  );
}
