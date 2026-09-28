/**
 * Leadership roster.
 *
 * Leave `github` / `linkedin` unset (or empty strings) to hide those links
 * on a card.
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
    name: "Srivatsan Balaji",
    role: "Founder & President",
    bio: "Leads the organization and sets its overall direction, from partnerships and expansion to the coordination of major events.",
    responsibilities: [
      "Leads the organization",
      "Sets overall direction",
      "Organizes partnerships and expansion",
      "Coordinates major events",
      "Oversees leadership and long-term planning",
    ],
    initials: "SB",
  },
  {
    id: "ctf-technical-director",
    name: "Sidhanth Poduri",
    role: "CTF & Technical Director",
    bio: "Leads the design of CTF challenges and the organization's technical resources, and supports members preparing for CyberPatriot and NCL.",
    responsibilities: [
      "Leads development of CTF challenges",
      "Oversees cybersecurity curriculum and technical resources",
      "Helps organize workshops",
      "Supports CyberPatriot and NCL preparation",
    ],
    initials: "SP",
  },
  {
    id: "outreach-director",
    name: "Ronnie Routray",
    role: "Outreach Director",
    bio: "Leads student outreach and communications, helping students across participating schools find and join the community.",
    responsibilities: [
      "Leads student outreach and recruitment",
      "Manages communications with members",
      "Helps connect students across participating schools",
    ],
    initials: "RR",
  },
  {
    id: "operations-financial-director",
    name: "Anish Kisari",
    role: "Operations & Financial Management Director",
    bio: "Coordinates event logistics and manages the organization's finances, from budgeting to funding events and challenges.",
    responsibilities: [
      "Coordinates event logistics",
      "Manages organization finances and budgeting",
      "Handles funding, expenses, and reimbursements",
      "Supports resource planning for events",
    ],
    initials: "AK",
  },
];
