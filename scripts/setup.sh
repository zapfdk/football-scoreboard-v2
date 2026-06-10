#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${ROOT}/.venv"
APP_DIR="${ROOT}/football_scoreboard"

cd "${ROOT}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but not installed." >&2
  exit 1
fi

if ! command -v redis-cli >/dev/null 2>&1; then
  echo "Warning: redis-cli not found. Make sure Redis is installed and running on 127.0.0.1:6379."
elif ! redis-cli ping >/dev/null 2>&1; then
  echo "Warning: Redis is not responding on 127.0.0.1:6379. Start Redis before running the app."
fi

if [[ ! -d "${VENV}" ]]; then
  echo "Creating virtual environment at ${VENV}..."
  python3 -m venv "${VENV}"
fi

# shellcheck disable=SC1091
source "${VENV}/bin/activate"

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

cd "${APP_DIR}"

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" && -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]]; then
  echo "Creating superuser ${DJANGO_SUPERUSER_USERNAME}..."
  python manage.py shell <<EOF
from django.contrib.auth import get_user_model

User = get_user_model()
username = "${DJANGO_SUPERUSER_USERNAME}"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username,
        "${DJANGO_SUPERUSER_EMAIL:-admin@localhost}",
        "${DJANGO_SUPERUSER_PASSWORD}",
    )
    print(f"Created superuser: {username}")
else:
    print(f"Superuser already exists: {username}")
EOF
else
  echo "Skipping superuser creation."
  echo "Optional: export DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_PASSWORD=secret && ./scripts/setup.sh"
  echo "Or run: cd football_scoreboard && python manage.py createsuperuser"
fi

echo
echo "Setup complete."
echo "Start the server with: ./scripts/run-gunicorn.sh"
