# NOVA Cyber Network — CTF Platform

A full-stack, team-based Capture The Flag competition platform built for **NOVA Cyber Network**,
a student-led cybersecurity community connecting four Northern Virginia high schools (John Champe,
Academies of Loudoun, Lightridge, and Freedom). Built for **NOVA CTF 2026** (October 17–18, 2026)
and designed to support future competitions.

**Stack:** Django 5.1 + PostgreSQL (SQLite for local dev) + Tailwind CSS v4 + HTMX, deployed as a
single Render Web Service with a managed Postgres database.

---

## 1. Project structure

```
nova-cyber-network/
├── config/              # Django project settings, URLs, WSGI
├── accounts/            # Users, Profile, School, ApprovedMember (roster), auth views
├── competitions/        # Competition, Announcement, get_current_competition()
├── teams/                # Team, TeamMembership, TeamInvite, services (create/join/leave), leaderboard query
├── challenges/           # ChallengeCategory, Challenge, Attachment, Hint, Submission, Solve, scoring service
├── core/                 # Home, dashboard, rules, health check, custom admin dashboard, audit log
├── templates/            # Django templates (base.html + one dir per app)
├── static/
│   ├── css/input.css     # Tailwind source (theme tokens, components)
│   ├── css/output.css    # Built CSS (generated — see "Building CSS" below)
│   └── challenge_files/  # Starter challenge attachments, organized by category
├── build.sh               # Render build script (installs deps, builds CSS, migrates, seeds data)
├── render.yaml             # Render Blueprint (web service + managed Postgres)
├── requirements.txt
└── manage.py
```

---

## 2. Running locally

**Prerequisites:** Python 3.13 (3.11+ should work). No Node.js required — Tailwind is built with
the standalone CLI binary.

```bash
cd nova-cyber-network
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # edit values as needed; defaults work for local dev
python manage.py migrate
python manage.py seed_competition  # creates the NOVA CTF 2026 competition, categories, schools
python manage.py seed_challenges   # creates the 12 starter challenges
python manage.py createsuperuser   # or use `ensure_admin` — see section 8
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`. By default this uses a local SQLite file (`db.sqlite3`) — no
database server required. Static files (including Tailwind CSS) are served directly by Django's
dev-server static handler; no build step is needed for local development **unless** you edit
`static/css/input.css` (see below).

### Building CSS

Tailwind CSS is built with the [standalone CLI](https://tailwindcss.com/blog/standalone-cli) (no
Node.js needed). If you change `static/css/input.css` or add new Tailwind classes to a template,
rebuild the compiled CSS:

```bash
# macOS (Apple Silicon): tailwindcss-macos-arm64
# macOS (Intel):          tailwindcss-macos-x64
# Linux:                   tailwindcss-linux-x64
curl -sL -o bin/tailwindcss \
  https://github.com/tailwindlabs/tailwindcss/releases/download/v4.3.3/tailwindcss-macos-x64
chmod +x bin/tailwindcss
./bin/tailwindcss -i static/css/input.css -o static/css/output.css --minify
```

`build.sh` does this automatically on every Render deploy (downloading the Linux x64 binary), so
you only need to do this manually for local iteration.

---

## 3. Running tests

```bash
python manage.py test
```

46 tests across all apps cover: authentication, membership approval/claim flow, unauthorized admin
access, team creation/joining/leaving, team-size limits, team-lock-after-start, correct/incorrect/
duplicate flag submission, concurrent submissions (race-safety), point allocation, leaderboard
ordering (including the tie-break rule), and contest start/end restrictions.

---

## 4. Uploading to GitHub

```bash
git init
git add .
git commit -m "Initial commit: NOVA Cyber Network CTF platform"
git branch -M main
git remote add origin https://github.com/<your-org>/<your-repo>.git
git push -u origin main
```

---

## 5. Deploying to Render (Blueprint)

> For a more detailed, click-by-click walkthrough (including the cost tradeoffs of each Render
> plan and a troubleshooting table), see [DEPLOYMENT.md](DEPLOYMENT.md).

1. Push this repository to GitHub (see above).
2. In the Render dashboard: **New → Blueprint**, select your repository. Render will read
   `render.yaml` and propose a **Web Service** (`nova-ctf`) and a **PostgreSQL database**
   (`nova-ctf-db`).
3. **Before clicking Apply**, read the cost note at the top of `render.yaml`: it defaults both the
   web service and database to the paid **Starter** plan. This is intentional — the free web
   service tier cold-starts after inactivity (bad during a live event) and the free Postgres plan
   **expires 30 days after creation**. Switch either `plan:` to `free` if you accept those
   tradeoffs.
4. Click **Apply**. Render provisions the database, then builds and deploys the web service using
   `build.sh` (installs dependencies, builds CSS, runs `collectstatic`, runs migrations, seeds the
   competition + starter challenges).
5. Once live, set the three `DJANGO_SUPERUSER_*` environment variables in the Render dashboard
   (they're declared in `render.yaml` with `sync: false`, meaning Render won't auto-fill them —
   you set them yourself) and trigger a redeploy, or run them as a one-off job (see section 8).
6. Visit `https://<your-service>.onrender.com/health/` to confirm the app is live.

### Required environment variables

| Variable | Required | Notes |
|---|---|---|
| `SECRET_KEY` | Yes | Auto-generated by Render via `generateValue: true` |
| `DATABASE_URL` | Yes | Auto-wired by Render via `fromDatabase` |
| `IS_PRODUCTION` | Yes | Set to `true` by `render.yaml` — enables HTTPS redirect, secure cookies, HSTS |
| `DEBUG` | Yes | `false` in production |
| `ALLOWED_HOSTS` | Yes | Render also auto-adds `RENDER_EXTERNAL_HOSTNAME` |
| `DJANGO_SUPERUSER_USERNAME/EMAIL/PASSWORD` | For admin bootstrap | See section 8 |
| `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | Optional | Without these, password-reset emails are written to the log stream instead of actually sent |
| `CONTACT_EMAIL` | Optional | Shown in the footer and rules page |
| `DEFAULT_TEAM_SIZE_LIMIT` | Optional | Default max team size for new competitions |

The app binds to the `$PORT` Render provides, uses the Render-provided `DATABASE_URL` for
Postgres, and serves static files via WhiteNoise — no separate static file host needed. The
application has no dependency on local filesystem persistence (challenge attachments are checked
into the repository, not uploaded at runtime), so it remains fully functional after a Render
service restart.

---

## 6. Creating the initial administrator

Two options, both safe to run repeatedly (idempotent — never overwrites an existing password):

**Option A — management command (recommended for Render):**
Set `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD` as
environment variables, then run (locally, or as a Render one-off job / it also runs automatically
as part of `build.sh` on every deploy):
```bash
python manage.py ensure_admin
```

**Option B — interactive:**
```bash
python manage.py createsuperuser
```

No admin credentials are ever committed to the repository.

---

## 7. Importing the NOVA membership roster

1. Prepare a CSV with columns `name,email,school`.
2. Sign in as an admin, go to **Django Admin → Accounts → Approved members → Import CSV**
   (or `/admin/accounts/approvedmember/import-csv/`), and upload the file.
3. Existing emails are skipped automatically — safe to re-import an updated roster.
4. Each row gets a unique, private claim link (`/accounts/claim/<token>/`), visible only to admins
   in the roster's detail view. Share each member's link with them individually (e.g. via your
   existing club communication channel) — **no passwords are generated or emailed by this tool**,
   and imported member emails are never exposed publicly (they're masked in the admin list view
   too).
5. Members not on the roster can submit a request at `/accounts/request-access/`; their entry is
   held as `pending_review` until an admin approves it (Django Admin → Approved members → select →
   **Approve selected access requests**). Only then does their claim link start working.

---

## 8. Adding or editing CTF challenges

All challenge management happens in **Django Admin → Challenges → Challenges**
(`/admin/challenges/challenge/`):

- **Create/edit:** set title, category, difficulty, description, points, and the flag (the "Flag"
  field is write-only — leave it blank when editing to keep the current flag unchanged). Flags are
  hashed server-side and never exposed in the frontend, API responses, or logs.
- **Hints and attachments:** added inline on the challenge edit page. Attachments reference files
  checked into the repository under `static/challenge_files/<category-slug>/` — add your file to
  that folder (and commit it), then pick it from the dropdown on the challenge's attachment inline.
  This avoids depending on Render's ephemeral local disk for uploads (see "Known limitations").
- **Publish/unpublish/archive:** use the admin's bulk actions, or the `is_published` /
  `is_archived` checkboxes. Unpublished challenges are invisible to participants.
- Starter challenges can be (re-)seeded at any time with `python manage.py seed_challenges`
  (idempotent — only creates challenges that don't already exist by title).

Organizer-only solutions to the 12 starter challenges are kept in
[`docs/ORGANIZER_SOLUTIONS.md`](docs/ORGANIZER_SOLUTIONS.md) — **do not** commit this file's
contents anywhere participant-visible, and treat repository access accordingly.

---

## 9. Pre-event organizer testing checklist

- [ ] `python manage.py test` passes (46/46).
- [ ] Import the real roster CSV into a staging deploy and confirm claim links work for a sample
      member.
- [ ] Confirm `Competition.start_time` / `end_time` in Django Admin match the intended event
      window (stored in UTC; the admin and all templates display them in Eastern Time).
- [ ] Create a test team, join it from a second account with the invite code, and confirm the
      5-member cap is enforced.
- [ ] Submit a correct flag, an incorrect flag, and the same correct flag twice — confirm scoring
      and the "already solved" message behave as expected.
- [ ] Watch the leaderboard auto-refresh (~15s) and confirm the recent-activity feed updates.
- [ ] Verify challenges are invisible before `start_time` and flag submission is rejected before
      `start_time` and after `end_time`.
- [ ] Review `core/admin_submission_logs` for the flagged-repeated-attempts indicator.
- [ ] Export results CSV and submissions CSV from the admin overview and confirm they open
      cleanly in a spreadsheet.
- [ ] Confirm `/health/` returns `200` from the deployed Render URL.
- [ ] Rotate the real `DJANGO_SUPERUSER_PASSWORD` to something you haven't used elsewhere, and
      remove/disable any test accounts created during staging.
- [ ] Set `DEFAULT_FROM_EMAIL` / SMTP credentials if you want password-reset emails to actually be
      delivered during the event (otherwise, reset manually via Django Admin → Users → set
      password, and tell the participant their new password out of band).

---

## 10. Known limitations to resolve before real participants join

- **Challenge attachments require a redeploy to add.** Files must be committed to the repo under
  `static/challenge_files/`, not uploaded through the browser at runtime — intentional, since
  Render's local disk doesn't persist across restarts/deploys. For a future competition needing
  organizer-uploaded files without a redeploy, integrate an object storage service (e.g. Render
  Disks for a single persistent volume, or S3/R2/Cloudflare via `django-storages`) and swap
  `ChallengeAttachment` to reference that instead of a repo-relative path.
- **Hint "point cost" is modeled but not enforced.** `ChallengeHint.point_cost` exists in the
  schema for future dynamic-scoring competitions; this event uses fixed scoring and all hints are
  shown for free, per the brief.
- **Single current competition.** All participant-facing URLs (challenges, teams, leaderboard)
  operate on "the current competition" (live, else soonest upcoming, else most recently ended) via
  `get_current_competition()`. The data model fully supports multiple competitions (every relevant
  model has a `competition` FK), but routing isn't yet per-competition-slug — add that when a
  second competition is announced.
- **Password-reset email delivery depends on SMTP configuration.** Without `EMAIL_HOST` set, reset
  emails are written to the Render log stream rather than actually delivered — fine for
  admin-assisted resets, but set real SMTP credentials before relying on self-service reset at
  scale.
- **Scoreboard freeze is all-or-nothing.** Setting `Competition.scoreboard_frozen_at` freezes the
  *public* leaderboard view at that instant; it doesn't currently add an admin-only "true live"
  view for organizers to watch behind the freeze. Add one if you plan to use the freeze feature for
  a tense finish.

---

## 11. Security notes

- Flags are hashed with Django's password hasher (PBKDF2) server-side; the plaintext flag is never
  sent to the browser, stored in logs, or exposed via the Django admin after creation.
- All flag submissions and point awards happen inside a database transaction with row-level
  locking (`select_for_update`) on the team's score row, and a unique database constraint
  (`one_solve_per_team_per_challenge`) as a second line of defense — concurrent duplicate
  submissions cannot double-award points (see `challenges/tests.py::ConcurrentSubmissionTests`).
- Login, password reset, and flag submission are rate-limited (`django-ratelimit`).
- CSRF protection, secure/HTTP-only session cookies, HSTS, and SSL redirect are enabled in
  production (`IS_PRODUCTION=true`, set by `render.yaml`).
- All competition timing checks (`is_live`, `accepts_submissions`, etc.) run server-side against
  `timezone.now()` — the browser countdown on the homepage is cosmetic only.
