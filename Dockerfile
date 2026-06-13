FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 DJANGO_SETTINGS_MODULE=config.settings.production
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements/base.txt requirements/
RUN pip install --no-cache-dir -r requirements/base.txt
COPY . .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --worker-class gthread --threads 2 --timeout 120 --access-logfile - --error-logfile -

# Build timestamp
RUN echo "Build: $(date -u)" > /app/build.txt
