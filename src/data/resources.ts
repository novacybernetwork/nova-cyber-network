/**
 * Resource library.
 *
 * Each category maps to a section on the Resources page. `icon` must match a
 * key in the icon map in `src/components/resources/ResourceCategorySection.tsx`.
 * Swap any `resources` entry for your own curated links at any time.
 */

export type ResourceIcon =
  | "shield-check"
  | "trophy"
  | "flag"
  | "network"
  | "terminal"
  | "monitor"
  | "globe"
  | "lock"
  | "search"
  | "eye";

export interface ResourceLink {
  title: string;
  description: string;
  url: string;
}

export interface ResourceCategory {
  id: string;
  title: string;
  icon: ResourceIcon;
  description: string;
  resources: ResourceLink[];
}

export const resourceCategories: ResourceCategory[] = [
  {
    id: "cyberpatriot",
    title: "CyberPatriot",
    icon: "shield-check",
    description:
      "Preparation material for the national CyberPatriot competition, focused on securing Windows and Linux images.",
    resources: [
      {
        title: "CyberPatriot — Official Site",
        description: "Registration, season timeline, and official training resources.",
        url: "https://www.uscyberpatriot.org/",
      },
      {
        title: "CyberPatriot National Competition Rules",
        description: "The rules and scoring guidelines competitors are expected to follow.",
        url: "https://www.uscyberpatriot.org/competition/competition-overview",
      },
    ],
  },
  {
    id: "ncl",
    title: "National Cyber League",
    icon: "trophy",
    description:
      "Resources for individual and team preparation for NCL's scored, gamified cybersecurity challenges.",
    resources: [
      {
        title: "National Cyber League — Official Site",
        description: "Season schedule, game structure, and player resources.",
        url: "https://nationalcyberleague.org/",
      },
      {
        title: "NCL Individual Game Prep",
        description: "Overview of the categories tested in NCL's individual games.",
        url: "https://nationalcyberleague.org/season-prep",
      },
    ],
  },
  {
    id: "ctf-practice",
    title: "CTF Practice",
    icon: "flag",
    description:
      "Beginner-friendly platforms for practicing Capture the Flag challenges in legal, authorized environments.",
    resources: [
      {
        title: "picoCTF",
        description: "Beginner-friendly, always-on CTF challenges built by Carnegie Mellon.",
        url: "https://picoctf.org/",
      },
      {
        title: "OverTheWire Wargames",
        description: "Classic wargames for building Linux and security fundamentals.",
        url: "https://overthewire.org/wargames/",
      },
      {
        title: "CTFtime",
        description: "A calendar and archive of upcoming and past CTF competitions.",
        url: "https://ctftime.org/",
      },
    ],
  },
  {
    id: "networking",
    title: "Networking",
    icon: "network",
    description: "Fundamentals of how networks are built, configured, and defended.",
    resources: [
      {
        title: "Professor Messer — Network+",
        description: "Free, comprehensive networking fundamentals video course.",
        url: "https://www.professormesser.com/network-plus/",
      },
      {
        title: "Cisco Networking Academy",
        description: "Free introductory courses on networking and network security.",
        url: "https://www.netacad.com/",
      },
    ],
  },
  {
    id: "linux",
    title: "Linux",
    icon: "terminal",
    description: "Command-line fundamentals and system administration for Linux environments.",
    resources: [
      {
        title: "OverTheWire: Bandit",
        description: "A hands-on introduction to the Linux command line through small challenges.",
        url: "https://overthewire.org/wargames/bandit/",
      },
      {
        title: "Linux Journey",
        description: "A free, self-paced guide to Linux fundamentals.",
        url: "https://linuxjourney.com/",
      },
    ],
  },
  {
    id: "windows",
    title: "Windows",
    icon: "monitor",
    description: "Windows security concepts relevant to CyberPatriot-style hardening exercises.",
    resources: [
      {
        title: "Microsoft Learn — Windows Security",
        description: "Official documentation on Windows security features and best practices.",
        url: "https://learn.microsoft.com/en-us/windows/security/",
      },
    ],
  },
  {
    id: "web-security",
    title: "Web Security",
    icon: "globe",
    description: "Common web vulnerabilities and how to identify and remediate them, legally.",
    resources: [
      {
        title: "PortSwigger Web Security Academy",
        description: "Free, hands-on labs covering the OWASP Top 10 and beyond.",
        url: "https://portswigger.net/web-security",
      },
    ],
  },
  {
    id: "cryptography",
    title: "Cryptography",
    icon: "lock",
    description: "Applied cryptography concepts frequently tested in CTFs and NCL.",
    resources: [
      {
        title: "CryptoHack",
        description: "A gamified platform for learning cryptography through puzzles.",
        url: "https://cryptohack.org/",
      },
      {
        title: "Khan Academy — Cryptography",
        description: "A free, approachable introduction to cryptographic concepts.",
        url: "https://www.khanacademy.org/computing/computer-science/cryptography",
      },
    ],
  },
  {
    id: "digital-forensics",
    title: "Digital Forensics",
    icon: "search",
    description: "Investigative techniques for analyzing systems, files, and network traffic.",
    resources: [
      {
        title: "CyberDefenders",
        description: "Blue-team focused digital forensics and incident response challenges.",
        url: "https://cyberdefenders.org/",
      },
    ],
  },
  {
    id: "osint",
    title: "OSINT",
    icon: "eye",
    description: "Open-source intelligence gathering techniques used in investigative challenges.",
    resources: [
      {
        title: "OSINT Framework",
        description: "A curated directory of open-source intelligence tools and resources.",
        url: "https://osintframework.com/",
      },
    ],
  },
];
