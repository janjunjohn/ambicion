from pathlib import Path
import environ
import os
from django.contrib import messages

# Set Custom User
AUTH_USER_MODEL = 'manager.User'

# Login Error Page
LOGIN_URL = 'login/'


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v9m^lb1&(ch4vohml0i3g6sgw+uz$_^zd@#$l1%hzx7$n4wks6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ambicion',
    'client',
    'manager',
    'media',
    'widget_tweaks',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ambicion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ambicion.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

from socket import gethostname
hostname = gethostname()
print(f'#################### {hostname} ####################')
if "JUNs-MacBook-Pro.local" in hostname:
    # デバッグ環境
    # DEBUG = True 

    # Set Environment Variables
    env = environ.Env()
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    ALLOWED_HOSTS = ['*'] 
else:
    # 本番環境
    # DEBUG = False

    # Set Environment Variables
    env = environ.Env()
    environ.Env.read_env()

    import dj_database_url
    db_from_env = dj_database_url.config()
    DATABASES = {
        'default': dj_database_url.config()
    }
    ALLOWED_HOSTS = ['*']
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media Setting (images uploaded by manager)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_DIR = [
    os.path.join(BASE_DIR, 'media'),
]


# Mail Settings
SENDGRID_API_KEY = env('SENDGRID_API_KEY')
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Messages Styles
MESSAGE_TAGS = {
    messages.INFO: 'alert alert-info',
    messages.SUCCESS: 'alert alert-success',
    messages.WARNING: 'alert alert-warning',
    messages.ERROR: 'alert alert-danger',
}