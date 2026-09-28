import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Button } from "@/components/ui/Button";
import { EventCard } from "@/components/events/EventCard";
import { upcomingEvents } from "@/data/events";
import { ArrowRight } from "lucide-react";

export function UpcomingEventPreview() {
  const nextEvent = upcomingEvents[0];

  return (
    <section className="border-b border-border py-20 sm:py-28">
      <div className="mx-auto max-w-6xl px-6">
        <div className="flex flex-wrap items-end justify-between gap-6">
          <Reveal>
            <SectionHeading eyebrow="Upcoming Event" title="What's next" />
          </Reveal>
          <Reveal delayMs={80}>
            <Button href="/events" variant="ghost" icon={<ArrowRight className="h-4 w-4" />}>
              See all events
            </Button>
          </Reveal>
        </div>

        {nextEvent ? (
          <Reveal delayMs={120} className="mt-10 max-w-xl">
            <EventCard event={nextEvent} />
          </Reveal>
        ) : (
          <Reveal delayMs={120} className="mt-10">
            <p className="text-muted">
              No events are scheduled yet — check back soon, or fill out the interest form to
              hear first.
            </p>
          </Reveal>
        )}
      </div>
    </section>
  );
}
