# Образ приложения: Gunicorn слушает 8090 (снаружи — через nginx в compose).
# Старт от root: chown томов под appuser (иначе SQLite на /data падает с «unable to open database file»).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh && sed -i 's/\r$//' /docker-entrypoint.sh

USER root

EXPOSE 8090

ENTRYPOINT ["/docker-entrypoint.sh"]
