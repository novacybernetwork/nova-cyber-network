import type { MetadataRoute } from "next";
import { siteConfig } from "@/config/site";

// Required for `output: "export"` — this file has no per-request data, so
// it's safe to render once at build time.
export const dynamic = "force-static";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
    },
    sitemap: `${siteConfig.url}/sitemap.xml`,
  };
}
