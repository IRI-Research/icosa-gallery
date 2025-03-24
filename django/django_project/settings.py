"""
Django settings for icosa project.
Generated by 'django-admin startproject' using Django 4.2.11.
"""

import os
from pathlib import Path

import sentry_sdk
from boto3.s3.transfer import TransferConfig
from botocore.config import Config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
if os.environ.get("DJANGO_DISABLE_CACHE"):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
JWT_KEY = os.environ.get("JWT_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEPLOYMENT_ENV = os.environ.get("DEPLOYMENT_ENV")
DEPLOYMENT_HOST_WEB = os.environ.get("DEPLOYMENT_HOST_WEB")
DEPLOYMENT_HOST_API = os.environ.get("DEPLOYMENT_HOST_API")
DEBUG = False
if DEPLOYMENT_ENV in [
    "development",
    "local",
]:
    DEBUG = True

DEPLOYMENT_SCHEME = "http://" if os.environ.get("DEPLOYMENT_NO_SSL") else "https://"

SITE_ID = 1

ALLOWED_HOSTS = [
    "localhost",
    f"{DEPLOYMENT_HOST_WEB}",
]

CSRF_TRUSTED_ORIGINS = [
    f"{DEPLOYMENT_SCHEME}*.127.0.0.1",
    f"{DEPLOYMENT_SCHEME}{DEPLOYMENT_HOST_WEB}",
]


API_SERVER = DEPLOYMENT_HOST_WEB
if DEPLOYMENT_HOST_API:
    ALLOWED_HOSTS.append(f"{DEPLOYMENT_HOST_API}")
    CSRF_TRUSTED_ORIGINS.append(f"{DEPLOYMENT_SCHEME}{DEPLOYMENT_HOST_API}")
    API_SERVER = DEPLOYMENT_HOST_API

DJANGO_DEFAULT_FILE_STORAGE = os.environ.get("DJANGO_DEFAULT_FILE_STORAGE")
DJANGO_STORAGE_URL = os.environ.get("DJANGO_STORAGE_URL")
DJANGO_STORAGE_BUCKET_NAME = os.environ.get("DJANGO_STORAGE_BUCKET_NAME")
DJANGO_STORAGE_REGION_NAME = os.environ.get("DJANGO_STORAGE_REGION_NAME")
DJANGO_STORAGE_ACCESS_KEY = os.environ.get("DJANGO_STORAGE_ACCESS_KEY")
DJANGO_STORAGE_SECRET_KEY = os.environ.get("DJANGO_STORAGE_SECRET_KEY")
DJANGO_STORAGE_CUSTOM_DOMAIN = os.environ.get("DJANGO_STORAGE_CUSTOM_DOMAIN")
DJANGO_STORAGE_MEDIA_ROOT = os.environ.get("DJANGO_STORAGE_MEDIA_ROOT")

if (
    DJANGO_STORAGE_URL
    and DJANGO_STORAGE_BUCKET_NAME
    and DJANGO_STORAGE_REGION_NAME
    and DJANGO_STORAGE_ACCESS_KEY
    and DJANGO_STORAGE_SECRET_KEY
    and DJANGO_STORAGE_MEDIA_ROOT
):
    # Not using the STORAGES dict here as there is a bug in django-storages
    # that means we must set these separately.
    DEFAULT_FILE_STORAGE = DJANGO_DEFAULT_FILE_STORAGE
    AWS_DEFAULT_ACL = "public-read"
    AWS_ACCESS_KEY_ID = DJANGO_STORAGE_ACCESS_KEY
    AWS_SECRET_ACCESS_KEY = DJANGO_STORAGE_SECRET_KEY
    AWS_STORAGE_BUCKET_NAME = DJANGO_STORAGE_BUCKET_NAME
    AWS_S3_REGION_NAME = DJANGO_STORAGE_REGION_NAME
    AWS_S3_ENDPOINT_URL = DJANGO_STORAGE_URL
    if DJANGO_STORAGE_CUSTOM_DOMAIN:
        AWS_S3_CUSTOM_DOMAIN = DJANGO_STORAGE_CUSTOM_DOMAIN
    # Special case for Backblaze B2, which doesn't support `x-amz-checksum-*`
    # headers. See here (at time of writing):
    # https://www.backblaze.com/docs/cloud-storage-s3-compatible-api#unsupported-features
    if "backblazeb2.com" in DJANGO_STORAGE_URL:
        AWS_S3_CLIENT_CONFIG = Config(
            request_checksum_calculation="when_required",
        )
        # Effectively disable multipart uploads so that checksum calculation is
        # never required.
        AWS_S3_TRANSFER_CONFIG = TransferConfig(
            multipart_threshold=5368709120,  # 5GiB in bytes
        )

        MEDIA_ROOT = None
        MEDIA_URL = "/"  # unused with django-storages
        LOCAL_MEDIA_STORAGE = False
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
    MEDIA_URL = "/media/"
    DJANGO_STORAGE_MEDIA_ROOT = None
    LOCAL_MEDIA_STORAGE = True

STAFF_ONLY_ACCESS = os.environ.get("DJANGO_STAFF_ONLY_ACCESS")

# Application definition

APPEND_SLASH = False
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
INSTALLED_APPS = [
    "dal",
    "dal_select2",
    "django.contrib.auth",
    "icosa",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "compressor",
    "constance",
    "constance.backends.database",
    "corsheaders",
    "honeypot",
    "huey.contrib.djhuey",
    "import_export",
    "maintenance_mode",
    "silk",
]

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "silk.middleware.SilkyMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "icosa.middleware.redirect.RemoveSlashMiddleware",
    "maintenance_mode.middleware.MaintenanceModeMiddleware",
]

ROOT_URLCONF = "django_project.urls"
LOGIN_URL = "/login"

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
                "icosa.context_processors.settings_processor",
                "constance.context_processors.config",
                "icosa.context_processors.owner_processor",
                "icosa.context_processors.user_asset_likes_processor",
            ],
            "loaders": [
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST", "localhost")
EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_DEFAULT_FROM_EMAIL", "")
ADMIN_EMAIL = os.environ.get("DJANGO_ADMIN_EMAIL", None)

WSGI_APPLICATION = "django_project.wsgi.application"

PAGINATION_PER_PAGE = 40

ACCESS_TOKEN_EXPIRE_MINUTES = 20_160  # 2 weeks

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

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cors settings

CORS_ALLOW_ALL_ORIGINS = bool(os.environ.get("DJANGO_CORS_ALLOW_ALL_ORIGINS", False))

if os.environ.get("DJANGO_CORS_ALLOWED_ORIGINS", None) is not None:
    CORS_ALLOWED_ORIGINS = [
        x
        for x in os.environ.get(
            "DJANGO_CORS_ALLOWED_ORIGINS",
            "",
        ).split(",")
        if x
    ]

# Compressor settings

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

# Constance settings

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_CONFIG = {
    "BETA_MODE": (
        True,
        "Sets various text around the site, inc. the logo in the header",
        bool,
    ),
    "REGISTRATION_ALLOW_LIST": (
        "",
        "Comma-separated list of email addresses. When populated, will only allow these email addresses to register new accounts.",
        str,
    ),
    "EXTERNAL_MEDIA_CORS_ALLOW_LIST": (
        "",
        "Comma-separated list of domains who have set their CORS to allow fetching from this site's domain.",
        str,
    ),
    "HIDE_REPORTED_ASSETS": (
        True,
        "Assets that have been reported are removed from lister pages.",
        bool,
    ),
    "SIGNUP_OPEN": (
        False,
        "Enables the registration form.",
        bool,
    ),
    "WAITLIST_IF_SIGNUP_CLOSED": (
        False,
        "If Signup Open is False, this will enable the waitlist functionality. Does nothing if Signup Open is True.",
        bool,
    ),
}

# Debug Toolbar settings

DEBUG_TOOLBAR_ENABLED = True

DEBUG_TOOLBAR_URL_EXCLUDE: tuple[str] = ()

if DEBUG_TOOLBAR_ENABLED:
    INSTALLED_APPS = [
        "debug_toolbar",
    ] + INSTALLED_APPS

    MIDDLEWARE.remove(
        "django.middleware.gzip.GZipMiddleware",
    )
    MIDDLEWARE.remove(
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    )
    MIDDLEWARE.remove(
        "django.contrib.sessions.middleware.SessionMiddleware",
    )

    MIDDLEWARE = [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.middleware.gzip.GZipMiddleware",
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE

    INTERNAL_IPS = ["127.0.0.1"]

    def show_toolbar(request):
        """Put 'debug=on' or 'debug=1' in a query string to enable debugging for
        your current session. 'debug=off' will turn it off again.
        """
        if request.path in DEBUG_TOOLBAR_URL_EXCLUDE:
            # No point going any further if it's an excluded Url
            return False
        debug_flag = request.GET.get("debug")
        if debug_flag == "on" or debug_flag == "1":
            request.session["show_debug_toolbar"] = True
        elif debug_flag == "off" or debug_flag == "0":
            request.session["show_debug_toolbar"] = False
        session_debug = request.session.get("show_debug_toolbar", False)
        if request.user.is_superuser and session_debug:
            return True
        return False

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }

# Honeypot settings

HONEYPOT_FIELD_NAME = "asset_ref"

# Huey settings

HUEY = {
    "huey_class": "huey.SqliteHuey",  # Huey implementation to use.
    "results": True,  # Store return values of tasks.
    "store_none": False,  # If a task returns None, do not save to results.
    "immediate": False,
    "utc": True,  # Use UTC for all times internally.
    "consumer": {
        "workers": 1,
        "worker_type": "thread",
        "initial_delay": 0.1,  # Smallest polling interval, same as -d.
        "backoff": 1.15,  # Exponential backoff using this rate, -b.
        "max_delay": 10.0,  # Max possible polling interval, -m.
        "scheduler_interval": 1,  # Check schedule every second, -s.
        "periodic": True,  # Enable crontab feature.
        "check_worker_health": True,  # Enable worker health checks.
        "health_check_interval": 1,  # Check worker health every second.
    },
}

# Note: Huey has its own setting to disable the task queue, but this still
# calls the same code in userland. ENABLE_TASK_QUEUE is useful for excluding
# huey from the code path entirely.

ENABLE_TASK_QUEUE = os.environ.get("DJANGO_ENABLE_TASK_QUEUE", False)

# Maintenance Mode settings

MAINTENANCE_MODE = os.environ.get("DJANGO_MAINTENANCE_MODE", False)
MAINTENANCE_MODE_IGNORE_STAFF = True
MAINTENANCE_MODE_IGNORE_URLS = [
    "/admin/",
    "/device/",
    "/health",
    "/privacy-policy",
    "/terms",
    "/supporters",
    "/v1/",
]

# Ninja settings

NINJA_PAGINATION_PER_PAGE = 20

# Silk settings


def silky_perms(user):
    return user.is_superuser


def get_profile_intercept():
    percent = 0
    if os.environ.get("DJANGO_ENABLE_PROFILING", False):
        if DEBUG:
            percent = 100
        percent = 1
        try:
            percent = int(
                os.environ.get(
                    "DJANGO_PROFILING_INTERCEPT_PERCENT",
                    percent,
                )
            )
        except ValueError:
            pass
    return percent


SILKY_PYTHON_PROFILER = os.environ.get("DJANGO_ENABLE_PROFILING", False)
SILKY_INTERCEPT_PERCENT = get_profile_intercept()
SILKY_AUTHENTICATION = True  # User must login
SILKY_AUTHORISATION = True  # User must have permissions
SILKY_PERMISSIONS = silky_perms


# Sentry settings
SENTRY_DSN = os.environ.get("DJANGO_SENTRY_DSN", None)
if SENTRY_DSN is not None:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
    )
