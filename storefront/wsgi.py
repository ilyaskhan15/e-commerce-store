"""
WSGI config for storefront project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set settings module based on environment
if os.getenv('DJANGO_ENV') == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.production_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')

application = get_wsgi_application()
