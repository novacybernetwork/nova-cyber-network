# Deploying NOVA Cyber Network to Render — step by step

This walks through taking the project from this local folder to a live URL on Render, using the
`render.yaml` Blueprint already in this repo. Total time: ~15 minutes, plus a few minutes of Render
build time.

**Before you start, you'll need:**
- A [GitHub](https://github.com) account
- A [Render](https://render.com) account (free to create; the services themselves are paid — see
  Step 3)
- Git installed locally (`git --version` to check)

---

## Step 1 — Push the code to GitHub

From the `nova-cyber-network/` folder:

```bash
git init
git add .
git commit -m "Initial commit: NOVA Cyber Network CTF platform"
git branch -M main
```

Create a new **empty** repository on GitHub (don't initialize it with a README/license — this
repo already has one):
1. Go to [github.com/new](https://github.com/new)
2. Name it (e.g. `nova-cyber-network`), leave everything else unchecked, click **Create repository**
3. Copy the repo URL GitHub shows you (HTTPS form: `https://github.com/<you>/nova-cyber-network.git`)

Then push:

```bash
git remote add origin https://github.com/<you>/nova-cyber-network.git
git push -u origin main
```

Confirm by refreshing the GitHub page — you should see all the project files.

---

## Step 2 — Create the Blueprint on Render

1. Log into [dashboard.render.com](https://dashboard.render.com).
2. Click **New** (top right) → **Blueprint**.
3. Connect your GitHub account if you haven't already, then select the `nova-cyber-network`
   repository you just pushed.
4. Render reads `render.yaml` from the repo root automatically and shows you a preview of what it
   will create:
   - A **Web Service** named `nova-ctf`
   - A **PostgreSQL database** named `nova-ctf-db`

Don't click **Apply** yet — read Step 3 first.

---

## Step 3 — Understand the cost before applying

`render.yaml` sets both the web service (`plan: starter`) and the database (`plan: 0.1c-256mb`,
Render's current ID for the same tier formerly called Postgres "Starter") to a paid plan — roughly
$7/month each at time of writing. This is intentional, not an oversight:

| Plan | Free tier risk | Why the paid tier is used here |
|---|---|---|
| Web service | Spins down after ~15 min idle; the next request takes 30-60s to "cold start" | A live 48-hour competition can't have a participant's first request time out |
| PostgreSQL | **Deleted automatically 30 days after creation** | You'd lose all registrations/scores if the DB expires mid-event |

If you want to test the Blueprint itself for free first (e.g. a dry run weeks before the event),
edit `render.yaml` and change `plan: starter` to `plan: free` for the `web` service, and/or
`plan: 0.1c-256mb` to `plan: free` for the database — but switch both back before the real event,
and don't let a free database sit around for 30 days before the competition.

Render renamed its compute plan IDs in August 2026 (legacy names like `starter`/`standard`/`pro`
became `<cpu>c-<ram>` IDs like `0.5c-512mb`/`1c-2g`). The legacy web service name `starter` still
works, but Render's dashboard now rejects legacy Postgres plan names for *newly created* databases
— hence the database using `0.1c-256mb` instead of `starter`. If Render's Blueprint UI flags
either plan value as invalid when you apply it, check
[Render's current compute plan docs](https://render.com/docs/compute-plans) for the latest IDs —
plan naming is the one part of this setup most likely to drift after this was written.

---

## Step 4 — Apply the Blueprint

1. Click **Apply**.
2. Render provisions the Postgres database first, then builds the web service by running
   `build.sh`, which:
   - installs Python dependencies
   - downloads the Tailwind CLI and builds production CSS
   - runs `collectstatic`
   - runs database migrations
   - seeds the competition, categories, schools, and the 12 starter challenges (all idempotent —
     safe to happen on every deploy)
3. Watch the build log in the Render dashboard. First build typically takes 2-5 minutes.
4. When it says **Live**, open the service URL Render gives you (something like
   `https://nova-ctf.onrender.com`).

---

## Step 5 — Verify the deploy

Visit `https://<your-service>.onrender.com/health/` — you should see:

```json
{"status": "ok", "database": true}
```

Then visit the homepage itself and confirm the countdown/stats render (they will show 0
participants/teams/solves and 12 challenges until you start inviting people).

---

## Step 6 — Create the admin account

`render.yaml` declares three environment variables for this but deliberately leaves them unset
(`sync: false`) so you set them yourself rather than committing credentials:

1. In the Render dashboard, open the `nova-ctf` service → **Environment**.
2. Add:
   - `DJANGO_SUPERUSER_USERNAME` — e.g. `admin`
   - `DJANGO_SUPERUSER_EMAIL` — your email
   - `DJANGO_SUPERUSER_PASSWORD` — a strong, unique password
3. Save changes — Render will automatically redeploy. On that deploy, `build.sh` runs
   `python manage.py ensure_admin`, which creates the account (and is safe to leave these vars set
   permanently — it never overwrites an existing account's password on later deploys).
4. Sign in at `https://<your-service>.onrender.com/accounts/login/` with that username/password,
   then confirm you can reach `/manage/` (the custom admin dashboard) and `/admin/` (Django admin).

---

## Step 7 — Import the NOVA membership roster

1. Prepare a CSV with header `name,email,school` — one row per existing NOVA Cyber Network member.
2. While signed in as admin, go to `/admin/accounts/approvedmember/import-csv/` (or click **Import
   CSV** from the Approved Members list in Django admin).
3. Upload the file. Existing emails are skipped automatically, so it's safe to re-upload an
   updated roster later.
4. Each imported member gets a private claim link
   (`https://<your-service>.onrender.com/accounts/claim/<token>/`), visible only to admins on that
   member's detail page in Django admin. Share each person's link with them individually — no
   passwords are generated or emailed by the platform.

---

## Step 8 — Double-check the competition window and challenges

Everything is pre-seeded for **NOVA CTF 2026, Oct 24 00:00 → Oct 26 00:00 America/New_York**
(submissions close at that instant, covering through 11:59 PM Oct 25 ET), with the 12 starter
challenges published. If you need to adjust anything:

- **Dates/registration/pause switch:** Django admin → Competitions → NOVA Cyber Network CTF 2026.
  Times are stored in UTC in the form but the admin list/detail views are what you edit directly —
  enter them in UTC (e.g. Oct 24 2026 12:00 AM ET = Oct 24 2026 04:00 AM UTC during EDT).
- **Add more challenges:** Django admin → Challenges → Challenges → **Add**. For attachments, the
  file must already exist in the repo under `static/challenge_files/<category>/` — commit it and
  redeploy before it'll show up in the attachment picker.
- **Rules page text:** Django admin → Competitions → (your competition) → `rules_text` field, one
  rule per line.

Run through the full [pre-event testing checklist](README.md#9-pre-event-organizer-testing-checklist)
in the README before announcing the URL to participants.

---

## Step 9 (optional) — Custom domain

If NOVA Cyber Network has its own domain:
1. Render dashboard → `nova-ctf` service → **Settings** → **Custom Domains** → add your domain and
   follow Render's DNS instructions (a CNAME or ALIAS record, depending on whether it's an apex
   domain or subdomain).
2. Once verified, add that domain to the `ALLOWED_HOSTS` environment variable (comma-separated with
   the existing values) and redeploy.

---

## Updating the live site later

Any time you push new commits to the `main` branch on GitHub, Render automatically rebuilds and
redeploys (this is the default Blueprint behavior — "Auto-Deploy" is on unless you turned it off).
No manual steps needed for routine code changes; `build.sh` re-runs migrations and the idempotent
seed commands every time, so it's safe.

---

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| Build fails downloading Tailwind CLI | Render's build network hiccup — click **Manual Deploy → Deploy latest commit** to retry |
| `DisallowedHost` error on the live URL | Double-check `ALLOWED_HOSTS` includes the right value; Render auto-injects `RENDER_EXTERNAL_HOSTNAME` which `settings.py` appends automatically, so this is rare |
| Site loads unstyled (no dark theme) | `collectstatic` didn't find `static/css/output.css` — confirm it wasn't accidentally removed from the repo (it's committed on purpose; see `.gitignore`'s comment) |
| Can't log in as admin after setting the env vars | Confirm the deploy that followed actually finished (check the **Events** tab), then check **Logs** for the `ensure_admin` output during that build |
| Password reset emails never arrive | Expected unless you've set `EMAIL_HOST`/`EMAIL_HOST_USER`/`EMAIL_HOST_PASSWORD` — otherwise emails are written to the service's log stream only. Reset manually via Django admin → Users in the meantime |
