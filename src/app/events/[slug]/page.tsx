import type { Metadata } from "next";
import Link from "next/link";
import Image from "next/image";
import { notFound } from "next/navigation";
import { ArrowLeft, CalendarDays, MapPin, Signal, Trophy, Users } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { PageHeader } from "@/components/layout/PageHeader";
import { events, getEventBySlug } from "@/data/events";

export function generateStaticParams() {
  return events.map((event) => ({ slug: event.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const event = getEventBySlug(slug);
  if (!event) return {};
  return {
    title: event.name,
    description: event.description ?? event.recap,
  };
}

export default async function EventDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const event = getEventBySlug(slug);
  if (!event) notFound();

  const isCompleted = event.status === "completed";

  return (
    <>
      <PageHeader
        eyebrow={isCompleted ? "Completed Event" : "Upcoming Event"}
        title={event.name}
        description={event.description}
      />

      <section className="py-20 sm:py-28">
        <div className="mx-auto max-w-4xl px-6">
          <Link
            href="/events"
            className="inline-flex items-center gap-2 text-sm font-medium text-muted hover:text-accent"
          >
            <ArrowLeft className="h-4 w-4" aria-hidden="true" />
            Back to all events
          </Link>

          <div className="mt-8 grid gap-4 sm:grid-cols-3">
            <Card hover={false} className="flex items-center gap-3">
              <CalendarDays className="h-5 w-5 shrink-0 text-accent" aria-hidden="true" />
              <div>
                <p className="text-xs text-muted">Date</p>
                <p className="text-sm font-medium text-foreground">{event.date}</p>
              </div>
            </Card>
            <Card hover={false} className="flex items-center gap-3">
              <MapPin className="h-5 w-5 shrink-0 text-accent" aria-hidden="true" />
              <div>
                <p className="text-xs text-muted">Location</p>
                <p className="text-sm font-medium text-foreground">{event.location}</p>
              </div>
            </Card>
            <Card hover={false} className="flex items-center gap-3">
              <Signal className="h-5 w-5 shrink-0 text-accent" aria-hidden="true" />
              <div>
                <p className="text-xs text-muted">Experience Level</p>
                <p className="text-sm font-medium text-foreground">{event.experienceLevel}</p>
              </div>
            </Card>
          </div>

          <div className="mt-8 flex flex-wrap gap-2">
            {event.topics.map((topic) => (
              <Badge key={topic}>{topic}</Badge>
            ))}
          </div>

          {!isCompleted && (
            <div className="mt-10 flex items-center gap-4 rounded-2xl border border-border bg-white/[0.02] p-6">
              <div>
                <p className="text-sm font-semibold text-foreground">
                  {event.registrationLabel ?? "Registration Coming Soon"}
                </p>
                <p className="mt-1 text-sm text-muted">
                  Join the Discord to be notified the moment registration opens.
                </p>
              </div>
            </div>
          )}

          {isCompleted && (
            <div className="mt-10 space-y-10">
              {(event.participantCount || event.schoolCount || event.challengeCount) && (
                <div className="grid grid-cols-3 gap-4">
                  {typeof event.participantCount === "number" && (
                    <Card hover={false} className="text-center">
                      <Users className="mx-auto h-5 w-5 text-accent" aria-hidden="true" />
                      <p className="mt-2 font-mono text-2xl font-semibold text-foreground">
                        {event.participantCount}
                      </p>
                      <p className="text-xs text-muted">Participants</p>
                    </Card>
                  )}
                  {typeof event.schoolCount === "number" && (
                    <Card hover={false} className="text-center">
                      <p className="font-mono text-2xl font-semibold text-foreground">
                        {event.schoolCount}
                      </p>
                      <p className="text-xs text-muted">Schools Represented</p>
                    </Card>
                  )}
                  {typeof event.challengeCount === "number" && (
                    <Card hover={false} className="text-center">
                      <p className="font-mono text-2xl font-semibold text-foreground">
                        {event.challengeCount}
                      </p>
                      <p className="text-xs text-muted">Challenges</p>
                    </Card>
                  )}
                </div>
              )}

              {event.recap && (
                <div>
                  <h2 className="text-xl font-semibold text-foreground">Recap</h2>
                  <p className="mt-3 text-pretty leading-relaxed text-muted">{event.recap}</p>
                </div>
              )}

              {event.lessonsLearned && (
                <div>
                  <h2 className="text-xl font-semibold text-foreground">Lessons Learned</h2>
                  <p className="mt-3 text-pretty leading-relaxed text-muted">
                    {event.lessonsLearned}
                  </p>
                </div>
              )}

              {event.winners && event.winners.length > 0 && (
                <div>
                  <h2 className="flex items-center gap-2 text-xl font-semibold text-foreground">
                    <Trophy className="h-5 w-5 text-accent" aria-hidden="true" />
                    Winners
                  </h2>
                  <ul className="mt-3 space-y-1 text-muted">
                    {event.winners.map((winner) => (
                      <li key={winner.place}>
                        <span className="font-medium text-foreground">{winner.place}:</span>{" "}
                        {winner.name}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {event.screenshots && event.screenshots.length > 0 && (
                <div>
                  <h2 className="text-xl font-semibold text-foreground">Screenshots</h2>
                  <div className="mt-4 grid gap-4 sm:grid-cols-2">
                    {event.screenshots.map((src) => (
                      <div
                        key={src}
                        className="relative aspect-video overflow-hidden rounded-xl border border-border"
                      >
                        <Image src={src} alt={`${event.name} screenshot`} fill className="object-cover" />
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {event.resources && event.resources.length > 0 && (
                <div>
                  <h2 className="text-xl font-semibold text-foreground">Writeups &amp; Resources</h2>
                  <ul className="mt-3 space-y-2">
                    {event.resources.map((resource) => (
                      <li key={resource.url}>
                        <a
                          href={resource.url}
                          target="_blank"
                          rel="noreferrer noopener"
                          className="text-sm font-semibold text-accent hover:underline"
                        >
                          {resource.title}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </section>
    </>
  );
}
