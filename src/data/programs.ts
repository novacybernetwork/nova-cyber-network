export type ProgramIcon =
  | "flag"
  | "presentation"
  | "shield-check"
  | "trophy"
  | "book-open"
  | "users";

export interface Program {
  title: string;
  description: string;
  icon: ProgramIcon;
}

/** "What We Do" — shown on the homepage and About page. */
export const programs: Program[] = [
  {
    title: "Capture the Flag Competitions",
    description: "Student-built CTFs that introduce teams to real security challenges in a structured, beginner-friendly format.",
    icon: "flag",
  },
  {
    title: "Cybersecurity Workshops",
    description: "Hands-on sessions covering practical skills across offense, defense, and everything in between.",
    icon: "presentation",
  },
  {
    title: "CyberPatriot Preparation",
    description: "Practice and guidance for teams competing in the CyberPatriot national competition.",
    icon: "shield-check",
  },
  {
    title: "National Cyber League Preparation",
    description: "Support for students preparing for NCL's individual and team games.",
    icon: "trophy",
  },
  {
    title: "Technical Resources",
    description: "A growing library of curated, legal, and authorized learning material for every skill level.",
    icon: "book-open",
  },
  {
    title: "Cross-School Community",
    description: "Connecting cybersecurity-interested students across multiple schools into one community.",
    icon: "users",
  },
];

/** Technical areas events and workshops can cover. */
export const focusAreas: string[] = [
  "Linux",
  "Windows Security",
  "Networking",
  "Cryptography",
  "Web Security",
  "Digital Forensics",
  "OSINT",
  "Scripting",
  "System Administration",
];
