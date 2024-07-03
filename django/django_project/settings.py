"""
Django settings for icosa project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
JWT_KEY = os.environ.get("JWT_SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEPLOYMENT_ENV = os.environ.get("DEPLOYMENT_ENV")
DEPLOYMENT_HOST_DJANGO = os.environ.get("DEPLOYMENT_HOST_DJANGO")
DEBUG = False
if DEPLOYMENT_ENV in [
    "development",
    "local",
]:
    DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    f"{DEPLOYMENT_HOST_DJANGO}",
]

CSRF_TRUSTED_ORIGINS = [
    f"https://{DEPLOYMENT_HOST_DJANGO}",
    "https://*.127.0.0.1",
]

DJANGO_STORAGE_URL = os.environ.get("DJANGO_STORAGE_URL")
DJANGO_STORAGE_BUCKET_NAME = os.environ.get("DJANGO_STORAGE_BUCKET_NAME")
DJANGO_STORAGE_REGION_NAME = os.environ.get("DJANGO_STORAGE_REGION_NAME")
DJANGO_STORAGE_ACCESS_KEY = os.environ.get("DJANGO_STORAGE_ACCESS_KEY")
DJANGO_STORAGE_SECRET_KEY = os.environ.get("DJANGO_STORAGE_SECRET_KEY")

if (
    DJANGO_STORAGE_URL
    and DJANGO_STORAGE_BUCKET_NAME
    and DJANGO_STORAGE_REGION_NAME
    and DJANGO_STORAGE_ACCESS_KEY
    and DJANGO_STORAGE_SECRET_KEY
):
    DEFAULT_FILE_STORAGE = "storages.backends.s3.S3Storage"
    AWS_DEFAULT_ACL = "public-read"
    AWS_ACCESS_KEY_ID = DJANGO_STORAGE_ACCESS_KEY
    AWS_SECRET_ACCESS_KEY = DJANGO_STORAGE_SECRET_KEY
    AWS_STORAGE_BUCKET_NAME = DJANGO_STORAGE_BUCKET_NAME
    AWS_S3_REGION_NAME = DJANGO_STORAGE_REGION_NAME
    AWS_S3_ENDPOINT_URL = DJANGO_STORAGE_URL
    # STORAGES = {
    #     "default": {
    #         # TODO make this configurable
    #         "BACKEND": "storages.backends.s3.S3Storage",
    #         "OPTIONS": {
    #             "bucket_name": DJANGO_STORAGE_BUCKET_NAME,
    #             "default_acl": "public-read",
    #             "region_name": DJANGO_STORAGE_REGION_NAME,
    #             "endpoint_url": DJANGO_STORAGE_URL,
    #             "access_key": DJANGO_STORAGE_ACCESS_KEY,
    #             "secret_key": DJANGO_STORAGE_SECRET_KEY,
    #         },
    #     },
    #     "staticfiles": {
    #         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    #     },
    # }
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    # STORAGES = {
    #     "default": {
    #         "BACKEND": "django.core.files.storage.FileSystemStorage",
    #     },
    #     "staticfiles": {
    #         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    #     },
    # }
# Application definition

INSTALLED_APPS = [
    # "admin_tools",
    # "admin_tools.dashboard",
    "icosa",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "compressor",
    # "main_dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_project.urls"
LOGIN_URL = "/login/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "icosa.context_processors.owner_processor",
            ],
            "loaders": [
                "django.template.loaders.app_directories.Loader",
                "admin_tools.template_loaders.Loader",
            ],
        },
    },
]

WSGI_APPLICATION = "django_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

# Media files
# TODO make this configurable based on file storage. We should have an absolute
# path for local storage and a root-relative path for storages such as s3.
MEDIA_ROOT = "icosa"
# MEDIA_URL = "..."  # unused with django-storages

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Admin Tools settings

ADMIN_TOOLS_INDEX_DASHBOARD = "main_dashboard.dashboard.MainDashboard"

# Compressor settings

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

# Ninja settings

NINJA_PAGINATION_PER_PAGE = 20
