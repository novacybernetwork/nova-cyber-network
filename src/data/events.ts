/**
 * Events data.
 *
 * Add new events to the `events` array. Each event needs a unique `slug` —
 * that becomes its detail page at `/events/<slug>`.
 *
 * Set `status` to "upcoming" while an event is being planned/announced, and
 * flip it to "completed" once it has happened. Completed events can carry a
 * full recap — participant counts, winners, screenshots, and writeup links —
 * none of which needs to be filled in until the event actually happens.
 */

export type EventStatus = "upcoming" | "completed";

export interface EventWriteup {
  title: string;
  url: string;
}

export interface EventWinner {
  place: string;
  name: string;
}

export interface CyberEvent {
  slug: string;
  name: string;
  status: EventStatus;
  /** Display string. Use "[DATE TBD]" until a real date is set. */
  date: string;
  location: string;
  experienceLevel: string;
  description: string;
  topics: string[];
  /** Shown as the CTA button label on upcoming events. */
  registrationLabel?: string;
  registrationUrl?: string;

  // --- Completed-event recap fields (all optional; fill in after the event) ---
  participantCount?: number;
  schoolCount?: number;
  challengeCount?: number;
  categories?: string[];
  winners?: EventWinner[];
  recap?: string;
  lessonsLearned?: string;
  screenshots?: string[];
  resources?: EventWriteup[];
}

export const events: CyberEvent[] = [
  {
    slug: "ctf-1",
    name: "CTF #1",
    status: "upcoming",
    date: "October 6, 2026",
    location: "Online",
    experienceLevel: "Beginner to Intermediate",
    description:
      "Our first community Capture the Flag competition will introduce students to a variety of cybersecurity challenges in a beginner-friendly environment.",
    topics: ["Linux", "Networking", "Cryptography", "Web Security", "Digital Forensics"],
    registrationLabel: "Registration Coming Soon",
  },
];

export const upcomingEvents = events.filter((event) => event.status === "upcoming");
export const pastEvents = events.filter((event) => event.status === "completed");

export function getEventBySlug(slug: string): CyberEvent | undefined {
  return events.find((event) => event.slug === slug);
}
