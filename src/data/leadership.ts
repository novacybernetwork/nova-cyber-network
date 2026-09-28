/**
 * Leadership roster.
 *
 * Replace the placeholder `name` fields with real names when ready. Leave
 * `github` / `linkedin` as empty strings to hide those links on a card.
 */

export interface LeadershipMember {
  id: string;
  name: string;
  role: string;
  bio: string;
  responsibilities: string[];
  initials: string;
  github?: string;
  linkedin?: string;
}

export const leadership: LeadershipMember[] = [
  {
    id: "president",
    name: "[YOUR NAME]",
    role: "Founder & President",
    bio: "Leads the organization and sets its overall direction, from partnerships and expansion to the coordination of major events.",
    responsibilities: [
      "Leads the organization",
      "Sets overall direction",
      "Organizes partnerships and expansion",
      "Coordinates major events",
      "Oversees leadership and long-term planning",
    ],
    initials: "YN",
    github: "",
    linkedin: "",
  },
  {
    id: "ctf-technical-director",
    name: "[TECHNICAL DIRECTOR NAME]",
    role: "CTF & Technical Director",
    bio: "Leads the design of CTF challenges and the organization's technical resources, and supports members preparing for CyberPatriot and NCL.",
    responsibilities: [
      "Leads development of CTF challenges",
      "Oversees cybersecurity curriculum and technical resources",
      "Helps organize workshops",
      "Supports CyberPatriot and NCL preparation",
    ],
    initials: "TD",
    github: "",
    linkedin: "",
  },
  {
    id: "outreach-operations-director",
    name: "[OPERATIONS DIRECTOR NAME]",
    role: "Outreach & Operations Director",
    bio: "Manages member communications and event logistics, and leads outreach so students across participating schools can find and join the community.",
    responsibilities: [
      "Manages communications with members",
      "Coordinates event logistics",
      "Leads student outreach and recruitment",
      "Helps connect students across participating schools",
    ],
    initials: "OD",
    github: "",
    linkedin: "",
  },
];
