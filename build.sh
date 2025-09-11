#!/usr/bin/env bash
# Exit on error
set -o errexit

# Set Django environment
export DJANGO_ENV=production

# Install dependencies
pip install -r requirements.txt

# Collect static files (no database connection needed)
python manage.py collectstatic --noinput --settings=storefront.production_settings

echo "Build completed successfully. Database migrations will run at startup."
