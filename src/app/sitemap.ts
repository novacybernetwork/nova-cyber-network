import type { MetadataRoute } from "next";
import { siteConfig } from "@/config/site";
import { events } from "@/data/events";

// Required for `output: "export"` — this file has no per-request data, so
// it's safe to render once at build time.
export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  const staticRoutes = [
    "",
    "/about",
    "/events",
    "/resources",
    "/leadership",
    "/join",
    "/code-of-conduct",
  ].map((route) => ({
    url: `${siteConfig.url}${route}`,
    lastModified: new Date(),
  }));

  const eventRoutes = events.map((event) => ({
    url: `${siteConfig.url}/events/${event.slug}`,
    lastModified: new Date(),
  }));

  return [...staticRoutes, ...eventRoutes];
}
