import Link from "next/link";
import { CalendarDays, Trophy, Users } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import type { CyberEvent } from "@/data/events";

/**
 * Card for a completed event recap. Not in use yet since no events have run,
 * but wired up so the Events page can render real recaps the moment
 * `status: "completed"` events are added to `src/data/events.ts`.
 */
export function CompletedEventCard({ event }: { event: CyberEvent }) {
  return (
    <Card className="flex h-full flex-col">
      <span className="inline-flex w-fit items-center rounded-full border border-border bg-white/[0.03] px-3 py-1 text-xs font-semibold tracking-wide text-muted uppercase">
        Completed
      </span>

      <h3 className="mt-4 text-xl font-semibold text-foreground">{event.name}</h3>
      {event.recap && (
        <p className="mt-2 text-sm leading-relaxed text-muted">{event.recap}</p>
      )}

      <dl className="mt-5 grid grid-cols-2 gap-3 text-sm text-muted">
        <div className="flex items-center gap-2">
          <CalendarDays className="h-4 w-4 text-accent" aria-hidden="true" />
          <dd>{event.date}</dd>
        </div>
        {typeof event.participantCount === "number" && (
          <div className="flex items-center gap-2">
            <Users className="h-4 w-4 text-accent" aria-hidden="true" />
            <dd>{event.participantCount} participants</dd>
          </div>
        )}
        {event.winners && event.winners.length > 0 && (
          <div className="col-span-2 flex items-center gap-2">
            <Trophy className="h-4 w-4 text-accent" aria-hidden="true" />
            <dd>{event.winners.map((w) => `${w.place}: ${w.name}`).join(", ")}</dd>
          </div>
        )}
      </dl>

      {event.categories && event.categories.length > 0 && (
        <div className="mt-5 flex flex-wrap gap-2">
          {event.categories.map((category) => (
            <Badge key={category}>{category}</Badge>
          ))}
        </div>
      )}

      <div className="mt-6">
        <Link
          href={`/events/${event.slug}`}
          className="text-sm font-semibold text-accent hover:underline"
        >
          Read the recap
        </Link>
      </div>
    </Card>
  );
}
