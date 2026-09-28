import {
  Eye,
  ExternalLink,
  Flag,
  Globe,
  Lock,
  Monitor,
  Network,
  Search,
  ShieldCheck,
  Terminal,
  Trophy,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Reveal } from "@/components/ui/Reveal";
import type { ResourceCategory, ResourceIcon } from "@/data/resources";

const iconMap: Record<ResourceIcon, typeof Flag> = {
  "shield-check": ShieldCheck,
  trophy: Trophy,
  flag: Flag,
  network: Network,
  terminal: Terminal,
  monitor: Monitor,
  globe: Globe,
  lock: Lock,
  search: Search,
  eye: Eye,
};

export function ResourceCategorySection({
  category,
  delayMs = 0,
}: {
  category: ResourceCategory;
  delayMs?: number;
}) {
  const Icon = iconMap[category.icon];

  return (
    <Reveal delayMs={delayMs}>
      <Card hover={false} className="h-full">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-border bg-accent-soft text-accent">
            <Icon className="h-5 w-5" aria-hidden="true" />
          </div>
          <h3 className="text-base font-semibold text-foreground">{category.title}</h3>
        </div>
        <p className="mt-4 text-sm leading-relaxed text-muted">{category.description}</p>

        <ul className="mt-5 space-y-3 border-t border-border pt-4">
          {category.resources.map((resource) => (
            <li key={resource.title}>
              <a
                href={resource.url}
                target="_blank"
                rel="noreferrer noopener"
                className="group flex items-start justify-between gap-2 text-sm font-medium text-foreground hover:text-accent"
              >
                <span>{resource.title}</span>
                <ExternalLink
                  className="mt-0.5 h-3.5 w-3.5 shrink-0 text-muted transition-colors group-hover:text-accent"
                  aria-hidden="true"
                />
              </a>
              <p className="mt-0.5 text-xs leading-relaxed text-muted">{resource.description}</p>
            </li>
          ))}
        </ul>
      </Card>
    </Reveal>
  );
}
