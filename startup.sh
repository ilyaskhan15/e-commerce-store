#!/usr/bin/env bash
# startup.sh - Test database, run migrations and start the server

# Set Django environment
export DJANGO_ENV=production

# Test database connection first
echo "Testing database connection..."
python test_db_connection.py || echo "⚠️  Database connection test failed, continuing with startup..."

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --settings=storefront.production_settings || echo "⚠️  Database migrations failed, continuing with startup..."

# Populate sample data if using SQLite fallback
echo "Checking if sample data population is needed..."
python manage.py shell --settings=storefront.production_settings -c "
from django.conf import settings
from store.models import Collection
import subprocess
import sys

try:
    # Check if we're using SQLite and if we have data
    if 'sqlite' in settings.DATABASES['default']['ENGINE']:
        print('Using SQLite database')
        if Collection.objects.count() == 0:
            print('No collections found, populating sample data...')
            subprocess.run([sys.executable, 'manage.py', 'populate_sample_data', '--settings=storefront.production_settings'])
        else:
            print(f'Found {Collection.objects.count()} collections, skipping sample data')
    else:
        print('Using PostgreSQL database, skipping sample data population')
except Exception as e:
    print(f'Error checking database: {e}')
" || echo "⚠️  Sample data check failed, continuing with startup..."

# Create superuser if needed (only if database is available)
echo "Creating superuser if needed..."
python manage.py shell --settings=storefront.production_settings -c "
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    # Check for your username first
    if not User.objects.filter(username='ilyaskhann').exists():
        User.objects.create_superuser('ilyaskhann', 'ilyaskhann@gmail.com', 'ilyaskhan123')
        print('Superuser ilyaskhann created')
    # Fallback admin user
    elif not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Fallback admin superuser created')
    else:
        print('Superuser already exists')
except Exception as e:
    print(f'Could not create superuser: {e}')
" || echo "⚠️  Superuser creation failed, continuing with startup..."

# Start the server
echo "Starting Gunicorn server..."
exec gunicorn storefront.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --keep-alive 5 \
    --max-requests 1000 \
    --preload
