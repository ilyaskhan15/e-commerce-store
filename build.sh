#!/usr/bin/env bash
# Exit on error
set -o errexit

# Set Django environment
export DJANGO_ENV=production

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --settings=storefront.production_settings

# Apply database migrations
python manage.py migrate --settings=storefront.production_settings
