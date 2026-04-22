#!/bin/sh
set -e
mkdir -p /data /app/media /app/static
chown -R appuser:appuser /data /app/staticfiles /app/media /app/static 2>/dev/null || true
exec runuser -u appuser -- sh -c '
  set -e
  mkdir -p /data /app/media
  python manage.py migrate --noinput
  python manage.py collectstatic --noinput
  exec gunicorn --bind 0.0.0.0:8090 --workers 2 Astra.wsgi
'
