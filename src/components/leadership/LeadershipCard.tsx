import { Card } from "@/components/ui/Card";
import { GithubIcon, LinkedinIcon } from "@/components/ui/BrandIcons";
import type { LeadershipMember } from "@/data/leadership";

export function LeadershipCard({ member }: { member: LeadershipMember }) {
  return (
    <Card className="flex h-full flex-col">
      <div className="flex items-center gap-4">
        <div
          className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full border border-accent/30 bg-accent-soft font-mono text-lg font-semibold text-accent"
          aria-hidden="true"
        >
          {member.initials}
        </div>
        <div>
          <h3 className="text-base font-semibold text-foreground">{member.name}</h3>
          <p className="text-sm text-accent">{member.role}</p>
        </div>
      </div>

      <p className="mt-5 text-sm leading-relaxed text-muted">{member.bio}</p>

      <ul className="mt-5 space-y-1.5 text-sm text-muted">
        {member.responsibilities.map((item) => (
          <li key={item} className="flex gap-2">
            <span className="mt-2 h-1 w-1 shrink-0 rounded-full bg-accent" aria-hidden="true" />
            {item}
          </li>
        ))}
      </ul>

      {(member.github || member.linkedin) && (
        <div className="mt-5 flex items-center gap-3 border-t border-border pt-4">
          {member.github && (
            <a
              href={member.github}
              target="_blank"
              rel="noreferrer noopener"
              aria-label={`${member.name} on GitHub`}
              className="flex h-9 w-9 items-center justify-center rounded-full border border-border text-muted transition-colors hover:border-accent/40 hover:text-accent"
            >
              <GithubIcon className="h-4 w-4" aria-hidden="true" />
            </a>
          )}
          {member.linkedin && (
            <a
              href={member.linkedin}
              target="_blank"
              rel="noreferrer noopener"
              aria-label={`${member.name} on LinkedIn`}
              className="flex h-9 w-9 items-center justify-center rounded-full border border-border text-muted transition-colors hover:border-accent/40 hover:text-accent"
            >
              <LinkedinIcon className="h-4 w-4" aria-hidden="true" />
            </a>
          )}
        </div>
      )}
    </Card>
  );
}
