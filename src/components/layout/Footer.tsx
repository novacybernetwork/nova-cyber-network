import Link from "next/link";
import { MessageCircle, ShieldCheck } from "lucide-react";
import { GithubIcon, LinkedinIcon } from "@/components/ui/BrandIcons";
import { siteConfig } from "@/config/site";

export function Footer() {
  const year = new Date().getFullYear();
  const disclaimer = siteConfig.disclaimer.replace("{name}", siteConfig.name);

  const socials = [
    { label: "GitHub", href: siteConfig.links.github, icon: GithubIcon },
    { label: "Community Chat", href: siteConfig.links.communityChat, icon: MessageCircle },
    { label: "LinkedIn", href: siteConfig.links.linkedin, icon: LinkedinIcon },
  ].filter((social) => social.href);

  return (
    <footer className="relative border-t border-border">
      <div className="mx-auto max-w-6xl px-6 py-14">
        <div className="grid gap-10 md:grid-cols-[1.4fr_1fr_1fr]">
          <div>
            <Link href="/" className="flex items-center gap-2 text-sm font-semibold text-foreground">
              <ShieldCheck className="h-5 w-5 text-accent" aria-hidden="true" />
              {siteConfig.name}
            </Link>
            <p className="mt-3 max-w-sm text-sm leading-relaxed text-muted">
              Independent student-led cybersecurity community.
            </p>
            {socials.length > 0 && (
              <div className="mt-5 flex items-center gap-3">
                {socials.map(({ label, href, icon: Icon }) => (
                  <a
                    key={label}
                    href={href}
                    target="_blank"
                    rel="noreferrer noopener"
                    aria-label={label}
                    className="flex h-9 w-9 items-center justify-center rounded-full border border-border text-muted transition-colors hover:border-accent/40 hover:text-accent"
                  >
                    <Icon className="h-4 w-4" aria-hidden="true" />
                  </a>
                ))}
              </div>
            )}
          </div>

          <nav aria-label="Footer" className="text-sm">
            <p className="mb-3 font-mono text-xs font-medium tracking-[0.15em] text-muted uppercase">
              Site
            </p>
            <ul className="space-y-2">
              {siteConfig.footerLinks.map((link) => (
                <li key={link.href}>
                  <Link href={link.href} className="text-muted transition-colors hover:text-foreground">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>

          <div className="text-sm">
            <p className="mb-3 font-mono text-xs font-medium tracking-[0.15em] text-muted uppercase">
              Contact
            </p>
            <a
              href={`mailto:${siteConfig.email}`}
              className="text-muted transition-colors hover:text-foreground"
            >
              {siteConfig.email}
            </a>
          </div>
        </div>

        <div className="mt-12 border-t border-border pt-6">
          <p className="max-w-3xl text-xs leading-relaxed text-muted">{disclaimer}</p>
          <p className="mt-3 text-xs text-muted/70">
            © {year} {siteConfig.name}. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
