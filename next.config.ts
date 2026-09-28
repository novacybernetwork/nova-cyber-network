import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // The whole site is static (no database, no auth, no server-side data) —
  // export plain HTML/CSS/JS so it can be hosted on Render's free Static
  // Site tier (or any static host) instead of a paid always-on Node service.
  output: "export",
  images: {
    // Next's built-in image optimizer needs a server; static export can't
    // run it, so images are served as-is instead.
    unoptimized: true,
  },
};

export default nextConfig;
