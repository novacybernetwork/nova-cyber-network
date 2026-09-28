export const membershipDefinition =
  "Membership is open to high school students interested in cybersecurity, regardless of prior experience. Members may participate in competitions, workshops, practice sessions, technical discussions, and community events. There is no requirement to already have cybersecurity certifications or competition experience.";

export const membershipFlexibility =
  "Members are encouraged to participate regularly, but participation is flexible. Students may join individual events without committing to every activity.";

export interface JoinStep {
  title: string;
  description: string;
}

export const joinSteps: JoinStep[] = [
  {
    title: "Fill out the interest form",
    description: "Tell us a bit about yourself so we can keep you in the loop.",
  },
  {
    title: "Join the community chat",
    description:
      "We're setting up a group chat for real-time announcements and discussion — the interest form is the fastest way to get the invite as soon as it's live.",
  },
  {
    title: "Watch for upcoming events",
    description: "We'll post CTFs, workshops, and prep sessions as they're scheduled.",
  },
  {
    title: "Participate whenever you're available",
    description: "Join the events that work for you — there's no minimum commitment.",
  },
];
