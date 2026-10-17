#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
source venv/bin/activate
export DEBUG=True
python manage.py runserver 0.0.0.0:8000
