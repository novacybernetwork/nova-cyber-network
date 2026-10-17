#!/usr/bin/env bash
# Render build script. Runs on every deploy.
set -o errexit

echo "--- Installing Python dependencies ---"
pip install -r requirements.txt

echo "--- Building Tailwind CSS (production, minified) ---"
TAILWIND_VERSION="v4.3.3"
TAILWIND_BIN="./bin/tailwindcss-build"
mkdir -p bin
if [ ! -f "$TAILWIND_BIN" ]; then
  curl -sL -o "$TAILWIND_BIN" \
    "https://github.com/tailwindlabs/tailwindcss/releases/download/${TAILWIND_VERSION}/tailwindcss-linux-x64"
  chmod +x "$TAILWIND_BIN"
fi
"$TAILWIND_BIN" -i static/css/input.css -o static/css/output.css --minify

echo "--- Collecting static files ---"
python manage.py collectstatic --noinput

echo "--- Applying database migrations ---"
python manage.py migrate --noinput

echo "--- Ensuring admin account (no-op if env vars are unset) ---"
python manage.py ensure_admin

echo "--- Seeding competition configuration (idempotent) ---"
python manage.py seed_competition

echo "--- Seeding starter challenges (idempotent) ---"
python manage.py seed_challenges

echo "--- Build complete ---"
