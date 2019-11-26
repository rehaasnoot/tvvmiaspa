"""
Django settings for apps project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import json

PROJECT_NAME = "tvvmiaspa"
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

SECRETS_FILE="/tvv/secrets/tvvspa.settings.json"
SECRETS_JSON = json.load(open(SECRETS_FILE, 'r'))
SECRET_KEY = SECRETS_JSON.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
#ALLOWED_HOSTS = ['localhost', '192.168.0.3']
#ALLOWED_HOSTS += ['192.168.0.2']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'imagekit',
    'apps.tvvroot.apps.TVVRootConfig',
    'apps.user_registration.apps.RegistrationConfig'
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

ROOT_URLCONF = 'apps.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'apps.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SECRETS_JSON.get("DATABASE_LOCATION"), SECRETS_JSON.get("DATABASE_NAME")),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ROOT_URL='/'
LOGIN_URL='registration/login.html'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = '/tvv/media/' + PROJECT_NAME + '/static/'
STATIC_URL = '/static/'
#STATICFILES_DIRS = (STATIC_ROOT, )

GRAPHENE = { 'SCHEMA':'apps.tvvroot.schema.schema' }

UPLOAD_USER_IMAGE = 'user/images/'
UPLOAD_INSTRUMENT_BLEND = 'instrument/blend/'
UPLOAD_INSTRUMENT_IMAGE = 'instrument/images/'
UPLOAD_PLAYER_BLEND = 'player/blend/'
UPLOAD_PLAYER_IMAGE = 'player/images/'
UPLOAD_MUSIC_MIDI = 'music/midi/'
UPLOAD_MUSIC_AUDIO = 'music/audio/'
UPLOAD_VIDEO = 'music/video/'
# Media files (admin/user uploads)
MEDIA_ROOT = '/tvv/media/' + PROJECT_NAME + '/media/'
MEDIA_URL = '/media/'
