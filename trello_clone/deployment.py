import os
from pathlib import Path
from .settings import *
# from .settings import BASE_DIR
# from .settings import STATIC_URL, STATICFILES_DIRS

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['SECRET']
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']]
DEBUG = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS =[
    BASE_DIR / "static"
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

os.makedirs(BASE_DIR / 'static', exist_ok=True)
os.makedirs(BASE_DIR / 'staticfiles', exist_ok=True)

# Parse connection string properly
connection_string = os.environ.get('AZURE_POSTGRESQL_CONNECTIONSTRING', '')
if connection_string:
    parameters = {pair.split('=')[0]: pair.split('=')[1] for pair in connection_string.split(' ')}
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parameters['dbname'],
            'HOST': parameters['host'],
            'USER': parameters['user'],
            'PASSWORD': parameters['password'],
            'PORT': parameters.get('port', '5432'),
            'OPTIONS': {
                'sslmode': 'require',
                'sslcert': None,
            }
        }
    }
else:
    # Fallback to direct configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DBNAME', 'trelloclone-database'),
            'HOST': os.environ.get('DBHOST', 'trelloclone-server.postgres.database.azure.com'),
            'USER': os.environ.get('DBUSER', 'jwesthypnb'),
            'PASSWORD': os.environ.get('DBPASS', 'w9w9$ykq56nnkSlb'),
            'PORT': os.environ.get('DBPORT', '5432'),
            'OPTIONS': {
                'sslmode': 'require',
                'sslcert': None,
            }
        }
    }