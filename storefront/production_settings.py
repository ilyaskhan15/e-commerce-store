import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import base settings
from .settings import *

# Override production settings
DEBUG = False

# Remove Silk from production for database connection issues
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'silk']
MIDDLEWARE = [middleware for middleware in MIDDLEWARE if 'silk' not in middleware.lower()]

# Security settings
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '.onrender.com').split(',')
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'https://*.onrender.com').split(',')

# Database - use DATABASE_URL if available, otherwise individual env vars
import dj_database_url

if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
    }
elif all([os.getenv('DB_HOST'), os.getenv('DB_NAME'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD')]):
    # Use individual environment variables - try full hostname first
    db_host = os.getenv('DB_HOST')
    
    # If hostname doesn't contain domain, add it
    if '.' not in db_host:
        db_host = f"{db_host}.render-postgres.render.com"
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': db_host,
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
else:
    # Last resort - hardcoded with full hostname
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'storefront2',
            'USER': 'storefront_user',
            'PASSWORD': 'DwNnRY5evmcgWpZrhfsU5TwLgIJ6MhGj',
            'HOST': 'dpg-d31a20gd13ps73e825ag-a.render-postgres.render.com',
            'PORT': '5432',
        }
    }

# Add connection options for better reliability
DATABASES['default']['OPTIONS'] = {
    'connect_timeout': 30,
}

# Connection pooling and retry logic
DATABASES['default']['CONN_MAX_AGE'] = 600

# Static files with Whitenoise
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings for production
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True') == 'True'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
