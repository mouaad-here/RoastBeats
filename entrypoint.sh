#!/bin/sh

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Start Gunicorn
# Using 'exec' here ensures Gunicorn handles OS signals correctly
echo "Starting Gunicorn on port ${PORT:-8000}..."
exec gunicorn RoastBeats.wsgi:application \
    --workers 3 \
    --threads 4 \
    --worker-class gthread \
    --timeout 120 \
    --bind 0.0.0.0:${PORT:-8000}