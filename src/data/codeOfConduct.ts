export interface ConductRule {
  title: string;
  body: string;
}

export const conductRules: ConductRule[] = [
  {
    title: "Respect",
    body: "Treat all participants with respect regardless of skill level, experience, school, background, identity, or technical ability.",
  },
  {
    title: "Learn, Don't Attack",
    body: "Cybersecurity techniques discussed or practiced through the organization must only be used in authorized environments such as our challenges, CTF platforms, labs, or systems where the participant has explicit permission.",
  },
  {
    title: "No Unauthorized Activity",
    body: "Members may not use organization events, resources, or communication channels to encourage unauthorized access, disruption, harassment, credential theft, malware distribution, or attacks against real systems.",
  },
  {
    title: "Collaboration",
    body: "Helping others learn is encouraged. During competitive events, participants must follow the collaboration rules established for that specific event.",
  },
  {
    title: "Academic and Competitive Integrity",
    body: "Participants should follow the rules of CyberPatriot, NCL, CTFs, schools, and other competitions they participate in.",
  },
  {
    title: "Community Conduct",
    body: "Harassment, discrimination, targeted abuse, spam, or intentionally disruptive behavior is not allowed.",
  },
  {
    title: "Responsible Disclosure",
    body: "If a participant discovers a real security vulnerability, they should report it responsibly to the appropriate system owner rather than attempting to exploit it.",
  },
  {
    title: "Enforcement",
    body: "Leadership may remove participants from events or community spaces when necessary to maintain a safe, respectful, and legal environment.",
  },
];

export const conductAgreement =
  "Participation in the community indicates agreement to follow these expectations.";
