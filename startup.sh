#!/usr/bin/env bash
# startup.sh - Run migrations and start the server

# Set Django environment
export DJANGO_ENV=production

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --settings=storefront.production_settings

# Start the server
echo "Starting Gunicorn server..."
exec gunicorn storefront.wsgi:application --bind 0.0.0.0:$PORT
