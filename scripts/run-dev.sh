#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${ROOT}/.venv"
APP_DIR="${ROOT}/football_scoreboard"

if [[ ! -d "${VENV}" ]]; then
  echo "Virtual environment not found. Run ./scripts/setup.sh first." >&2
  exit 1
fi

# shellcheck disable=SC1091
source "${VENV}/bin/activate"

cd "${APP_DIR}"
exec python manage.py runserver "${GUNICORN_BIND:-127.0.0.1:8000}"
