import type { Metadata } from "next";
import { PageHeader } from "@/components/layout/PageHeader";
import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { EventCard } from "@/components/events/EventCard";
import { CompletedEventCard } from "@/components/events/CompletedEventCard";
import { pastEvents, upcomingEvents } from "@/data/events";

export const metadata: Metadata = {
  title: "Events",
  description:
    "Upcoming Capture the Flag competitions, workshops, and cybersecurity competition preparation.",
};

export default function EventsPage() {
  return (
    <>
      <PageHeader
        eyebrow="Events"
        title="Competitions, workshops, and prep sessions."
        description="Every event is designed to be approachable for first-timers while still offering something for experienced competitors."
      />

      <section className="border-b border-border py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-6">
          <Reveal>
            <SectionHeading eyebrow="Upcoming" title="Upcoming Events" />
          </Reveal>

          {upcomingEvents.length > 0 ? (
            <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {upcomingEvents.map((event, index) => (
                <Reveal key={event.slug} delayMs={index * 80}>
                  <EventCard event={event} />
                </Reveal>
              ))}
            </div>
          ) : (
            <Reveal delayMs={80} className="mt-10">
              <p className="text-muted">
                Nothing scheduled right now — check back soon or fill out the interest form to
                hear first.
              </p>
            </Reveal>
          )}
        </div>
      </section>

      <section className="py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-6">
          <Reveal>
            <SectionHeading eyebrow="Archive" title="Past Events" />
          </Reveal>

          {pastEvents.length > 0 ? (
            <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {pastEvents.map((event, index) => (
                <Reveal key={event.slug} delayMs={index * 80}>
                  <CompletedEventCard event={event} />
                </Reveal>
              ))}
            </div>
          ) : (
            <Reveal delayMs={80} className="mt-10 max-w-2xl">
              <p className="text-pretty leading-relaxed text-muted">
                No completed events yet. Event recaps, participation statistics, challenges,
                and results will be published here after each competition.
              </p>
            </Reveal>
          )}
        </div>
      </section>
    </>
  );
}
