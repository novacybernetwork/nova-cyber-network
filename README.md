# NOVA Cyber Network — Website

The public site for NOVA Cyber Network, an independent, student-led high school
cybersecurity community. Built with Next.js (App Router), TypeScript, and
Tailwind CSS. No database, no authentication, no backend — all real content
lives in a handful of plain data files so the site can be updated without
touching component code.

## Running it locally

```bash
npm install
npm run dev
```

Then open [http://localhost:3000](http://localhost:3000). Before shipping a
change, also run:

```bash
npm run lint
npm run build
```

`npm run build` must succeed with no errors before deploying.

## Where to edit things

Everything you're likely to need to update lives in `src/config/` and
`src/data/` — you should not need to touch component or page files for normal
content updates.

| What you want to change | File |
| --- | --- |
| Club name, tagline, mission copy, email, Discord/GitHub/Join-form URLs, nav links | [`src/config/site.ts`](src/config/site.ts) |
| Homepage statistics (members, schools, CTFs hosted, challenges released) | [`src/data/stats.ts`](src/data/stats.ts) |
| Leadership team (names, roles, bios, GitHub/LinkedIn links) | [`src/data/leadership.ts`](src/data/leadership.ts) |
| Events — upcoming and past, plus full recap data | [`src/data/events.ts`](src/data/events.ts) |
| Resource library links (CyberPatriot, NCL, CTF practice, etc.) | [`src/data/resources.ts`](src/data/resources.ts) |
| "What We Do" cards and focus-area tags | [`src/data/programs.ts`](src/data/programs.ts) |
| Membership copy and the "How to Join" steps | [`src/data/membership.ts`](src/data/membership.ts) |
| Code of Conduct rules | [`src/data/codeOfConduct.ts`](src/data/codeOfConduct.ts) |

### Club name

The organization name is a single config value:
`siteConfig.name` in `src/config/site.ts` (currently `"NOVA Cyber Network"`).
Change it there and it updates everywhere — navbar, footer, page titles, the
footer disclaimer, and social preview images.

### Still open

- **Community chat.** `links.communityChat` in `src/config/site.ts` is
  currently `""` — no platform has been picked yet (WhatsApp/GroupMe/Discord
  are all options). Every "Join the Chat" button on the site automatically
  shows a disabled "Community Chat Coming Soon" state while this is blank,
  and switches to a real link the moment you fill it in — no other code
  changes needed.
- **`siteConfig.url`** — still the placeholder Vercel-style URL. Update it
  once the site has a real deployed URL (see Deploying, below).

Everything else — email, interest form, leadership names/roles, member and
school counts, and the CTF #1 date — is filled in with real values in
`src/config/site.ts`, `src/data/leadership.ts`, `src/data/stats.ts`, and
`src/data/events.ts`.

### Adding a new event

Add an entry to the `events` array in `src/data/events.ts` with a unique
`slug` — that automatically creates a detail page at `/events/<slug>`. Set
`status: "upcoming"` while it's being planned, then flip it to
`status: "completed"` and fill in the recap fields (participant count,
schools represented, challenge count, winners, recap text, screenshots,
writeup links) once the event has actually happened. The Events page and
sitemap pick up new events automatically — no other code changes needed.

## Deploying

The site has no database, auth, or server-side logic, so `next build` exports
it as plain static HTML/CSS/JS into `out/` (set via `output: "export"` in
[`next.config.ts`](next.config.ts)). That means it can be hosted anywhere that
serves static files — no always-on Node server required.

### Render (Static Site)

1. This repo already lives on GitHub at
   [github.com/novacybernetwork/nova-cyber-network](https://github.com/novacybernetwork/nova-cyber-network).
2. In the Render dashboard, click **New > Static Site** and connect the repo.
   Since it's under the `novacybernetwork` organization, Render's repo picker
   will prompt you to grant its GitHub App access to that org the first time
   — approve it, then the repo will show up. (A [`render.yaml`](render.yaml)
   blueprint is already included — you can instead use **New > Blueprint** to
   have Render read it automatically.)
3. If configuring manually, set:
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `out`
4. Deploy. You'll get a free `*.onrender.com` URL; add a custom domain later
   from the site's Settings tab.
5. Update `siteConfig.url` in `src/config/site.ts` to match your real
   deployed URL (this feeds the sitemap and social-preview metadata), commit,
   and push — Render redeploys automatically on every push to your default
   branch.

Render's free Static Site tier has no cold starts and doesn't sleep (unlike
free Web Services), which is the right fit here since there's nothing dynamic
to run.

### Vercel (alternative)

Works the same way, static export included:

1. Push the repo to GitHub.
2. Go to [vercel.com/new](https://vercel.com/new) and import it — no config
   needed, Vercel auto-detects Next.js and serves the static export.
3. Update `siteConfig.url` the same way after your first deploy.

No environment variables are required on either host — the site has no
backend.

### If you later add something dynamic

If you eventually add a real API route, form handler, or anything else that
needs a server at request time, remove `output: "export"` from
`next.config.ts` and switch the Render service (or Vercel project) to a
Node/Web Service running `next build` + `next start` instead of a static
site.
