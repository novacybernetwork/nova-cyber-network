/**
 * Central site configuration.
 *
 * Edit the values in this file to rebrand or reconfigure the site without
 * touching any component code. Everything here is plain data.
 */

export const siteConfig = {
  /** The organization's display name. Shows up in the navbar, footer, and metadata. */
  name: "NOVA Cyber Network",

  /** Short form used in tight spaces (mobile nav, favicon alt text). */
  shortName: "NOVA Cyber",

  /** One-line homepage headline. */
  headline: "Learn Cybersecurity By Doing It.",

  /** Homepage subheadline. */
  subheadline:
    "An independent student-led community bringing high school students together through Capture the Flag competitions, workshops, and cybersecurity competition preparation.",

  /** Short mission statement used on the homepage. */
  missionShort:
    "Building a community where high school students learn cybersecurity by doing it.",

  /** Full mission statement used on the About page. */
  missionFull:
    "Our mission is to make hands-on cybersecurity accessible to high school students by creating opportunities to learn, compete, collaborate, and develop practical technical skills. Through student-built Capture the Flag competitions, workshops, and competition preparation, we aim to create a community where students of any experience level can grow their cybersecurity abilities.",

  /** "Why we exist" copy used on the About page. */
  whyWeExist:
    "Cybersecurity is best learned through practice. Many students are interested in the field but lack accessible opportunities to work through realistic challenges, meet other students with similar interests, or prepare for cybersecurity competitions. Our community was created to help close that gap through hands-on, student-led learning.",

  /** SEO description used across the site. */
  description:
    "An independent student-led cybersecurity community connecting high school students through CTF competitions, workshops, resources, and cybersecurity competition preparation.",

  /** Deployed site URL. Update after your first Render/Vercel deploy. */
  url: "https://nova-cyber-network.vercel.app",

  /** Public contact email. */
  email: "novacybernetwork@gmail.com",

  /** External links — paste your real URLs here once they exist. */
  links: {
    joinForm: "https://forms.gle/36yxFqjLJC29wZBW8",
    /**
     * Real-time community chat link. Empty until a platform is picked
     * (WhatsApp/GroupMe/Discord/etc.) — every "Join the Chat" button
     * automatically shows a "Coming Soon" state while this is blank, and
     * lights up the moment you paste a real invite link here.
     */
    communityChat: "",
    github: "https://github.com/vatsanbalaji/nova-cyber-network",
    linkedin: "",
  },

  /** Primary navigation, in order. */
  nav: [
    { label: "Home", href: "/" },
    { label: "About", href: "/about" },
    { label: "Events", href: "/events" },
    { label: "Resources", href: "/resources" },
    { label: "Leadership", href: "/leadership" },
    { label: "Join", href: "/join" },
  ],

  /** Footer link list. */
  footerLinks: [
    { label: "About", href: "/about" },
    { label: "Events", href: "/events" },
    { label: "Resources", href: "/resources" },
    { label: "Code of Conduct", href: "/code-of-conduct" },
    { label: "Join", href: "/join" },
  ],

  /** Legal disclaimer shown in the footer. `{name}` is replaced automatically. */
  disclaimer:
    "{name} is an independent student-led organization and is not officially affiliated with or endorsed by participating schools or school districts.",
} as const;

export type SiteConfig = typeof siteConfig;
