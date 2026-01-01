FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# create the static files for whitenoise

RUN python manage.py collectstatic --noinput --clear

# gunicorn
#CMD ["gunicorn", "RoastBeats.wsgi:application", "--workers", "2", "--threads", "4", "--worker-class", "gthread", "--timeout", "120", "--bind", "0.0.0.0:8000"]

# CMD sh -c "python manage.py migrate --noinput && \
#            gunicorn RoastBeats.wsgi:application \
#            --workers 3 \
#            --threads 4 \
#            --worker-class gthread \
#            --timeout 120 \
#            --bind 0.0.0.0:${PORT:-8000}"
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]