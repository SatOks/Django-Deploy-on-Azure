import os
from pathlib import Path
from .settings import *
# from .settings import BASE_DIR
# from .settings import STATIC_URL, STATICFILES_DIRS

BASE_DIR = Path(__file__).resolve().parent.parent

print("Using deployment settings")
print(f"Current directory: {BASE_DIR}")

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

# Direct database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'trelloclone-database',
        'HOST': 'trelloclone-server.postgres.database.azure.com',
        'USER': 'jwesthypnb@trelloclone-server',  # Add server suffix to username
        'PASSWORD': 'w9w9$ykq56nnkSlb',
        'PORT': '5432',
    }
}
