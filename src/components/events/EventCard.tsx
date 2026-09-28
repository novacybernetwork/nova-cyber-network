import Link from "next/link";
import { CalendarDays, MapPin, Signal } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import type { CyberEvent } from "@/data/events";

export function EventCard({ event }: { event: CyberEvent }) {
  return (
    <Card className="flex h-full flex-col">
      <div className="flex items-start justify-between gap-3">
        <span className="inline-flex items-center rounded-full border border-accent/30 bg-accent-soft px-3 py-1 text-xs font-semibold tracking-wide text-accent uppercase">
          Upcoming
        </span>
      </div>

      <h3 className="mt-4 text-xl font-semibold text-foreground">{event.name}</h3>
      <p className="mt-2 text-sm leading-relaxed text-muted">{event.description}</p>

      <dl className="mt-5 space-y-2 text-sm text-muted">
        <div className="flex items-center gap-2">
          <CalendarDays className="h-4 w-4 text-accent" aria-hidden="true" />
          <dt className="sr-only">Date</dt>
          <dd>{event.date}</dd>
        </div>
        <div className="flex items-center gap-2">
          <MapPin className="h-4 w-4 text-accent" aria-hidden="true" />
          <dt className="sr-only">Location</dt>
          <dd>{event.location}</dd>
        </div>
        <div className="flex items-center gap-2">
          <Signal className="h-4 w-4 text-accent" aria-hidden="true" />
          <dt className="sr-only">Experience level</dt>
          <dd>{event.experienceLevel}</dd>
        </div>
      </dl>

      <div className="mt-5 flex flex-wrap gap-2">
        {event.topics.map((topic) => (
          <Badge key={topic}>{topic}</Badge>
        ))}
      </div>

      <div className="mt-6 flex flex-1 flex-col items-start gap-3">
        <span className="w-fit cursor-not-allowed rounded-full border border-border bg-white/[0.02] px-4 py-2 text-xs font-semibold whitespace-nowrap text-muted">
          {event.registrationLabel ?? "Registration Coming Soon"}
        </span>
        <Link
          href={`/events/${event.slug}`}
          className="text-sm font-semibold text-accent hover:underline"
        >
          View details →
        </Link>
      </div>
    </Card>
  );
}
