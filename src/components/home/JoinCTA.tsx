import { ArrowRight, MessageCircle } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Reveal } from "@/components/ui/Reveal";
import { siteConfig } from "@/config/site";

export function JoinCTA() {
  return (
    <section className="relative overflow-hidden py-20 sm:py-28">
      <div className="bg-radial-glow pointer-events-none absolute inset-0" aria-hidden="true" />
      <Reveal className="relative mx-auto max-w-3xl px-6 text-center">
        <p className="font-mono text-xs font-medium tracking-[0.2em] text-accent uppercase">
          Join the Community
        </p>
        <h2 className="mt-4 text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
          Ready to start learning by doing?
        </h2>
        <p className="mx-auto mt-4 max-w-xl text-pretty text-base leading-relaxed text-muted">
          {siteConfig.missionShort}
        </p>
        <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <Button href="/join" variant="primary" icon={<ArrowRight className="h-4 w-4" />}>
            Join Interest Form
          </Button>
          <Button
            href={siteConfig.links.discord}
            variant="secondary"
            icon={<MessageCircle className="h-4 w-4" />}
          >
            Join Discord
          </Button>
        </div>
      </Reveal>
    </section>
  );
}
