import os
from pathlib import Path

import environ
from celery.schedules import crontab

from core.jazzmin_conf import *  # noqa

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
env.read_env(".env")
SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = ["*"]

STAGE = 'development'

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third
    'django_celery_beat',
    'debug_toolbar',
    "rest_framework",
    "drf_yasg",
    "corsheaders",
    "rosetta",
    # local
    "bots.common_bot",

]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework.authentication.SessionAuthentication",),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Ma'lumotlar bazasi uchun asosiy sozlamalar
if env.bool("DATABASE_POSTGRESQL"):
    DATABASES = {
        "default": {
            "ENGINE": env.str("DB_ENGINE", "django.db.backends.postgresql_psycopg2"),
            "NAME": env.str("DB_NAME"),
            "USER": env.str("DB_USER"),
            "PASSWORD": env.str("DB_PASSWORD"),
            "HOST": env.str("DB_HOST"),
            "PORT": env.str("DB_PORT"),
            "ATOMIC_REQUESTS": True,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            "ATOMIC_REQUESTS": True,
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
LANGUAGE_CODE = "uz"

TIME_ZONE = "Asia/Tashkent"
USE_I18N = True

USE_TZ = True
USE_L10N = True
LANGUAGES = [
    ("uz", "Uzbek"),
    ("ru", "Russian"),
    ("en", "English"),

]
MODELTRANSLATION_LANGUAGES = ("uz",)
MODELTRANSLATION_DEFAULT_LANGUAGE = "uz"
MODELTRANSLATION_FALLBACK_LANGUAGES = ("uz",)
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)
gettext = lambda s: s  # noqa

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = (BASE_DIR / "staticfiles",)

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{env.str('REDIS_URL', 'redis://localhost:6379/0')}",
        "KEY_PREFIX": "boilerplate",  # todo: you must change this with your project name or something else
    }
}

AUDITLOG_INCLUDE_ALL_MODELS = True

BROKER_URL = "redis://localhost:6379"
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Tashkent'
BROKER_CONNECTION_RETRY_ON_STARTUP = True

WEBHOOK_URL = env.str("WEBHOOK_URL")
CELERY_WEBHOOK = env.str("CELERY_WEBHOOK")

CELERY_BEAT_SCHEDULE = {

}
