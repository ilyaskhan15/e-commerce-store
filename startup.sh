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

# Create superuser if needed (only if database is available)
echo "Creating superuser if needed..."
python manage.py shell --settings=storefront.production_settings -c "
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Superuser created')
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
