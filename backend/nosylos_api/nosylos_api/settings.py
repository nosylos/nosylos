# flake8: noqa
import os
from datetime import timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")

SECRET_KEY = (
    "django-insecure-p(#$^&62v76luslm1!mqmsg-^drfd$cbj)brhkz$@)$1ug9^sp"
)

FRONTEND_URL = "http://127.0.0.1:3000"
CSRF_COOKIE_DOMAIN = "127.0.0.1"
if ENVIRONMENT == "staging":
    SECRET_KEY = os.environ.get("DJANGO_STAGING_SECRET", SECRET_KEY)
    FRONTEND_URL = "https://www.nosylos.com"
    CSRF_COOKIE_DOMAIN = ".nosylos.com"

if "RDS_HOSTNAME" in os.environ:
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1:3000",
    "127.0.0.1",
    "nosylos.com",
    "www.nosylos.com",
    "staging.nosylos.com",
    "staging.api.nosylos.com",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1",
    "https://nosylos.com",
    "https://www.nosylos.com",
    "https://staging.nosylos.com",
    "https://staging.api.nosylos.com",
]
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1",
    "https://nosylos.com",
    "https://www.nosylos.com",
    "https://staging.nosylos.com",
    "https://staging.api.nosylos.com",
]
CSRF_COOKIE_SECURE = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "user": "100/day",
    },
    "DEFAULT_RENDERER_CLASSES": [
        "utils.renderer.CamelCaseJsonRenderer",
        "utils.renderer.SnakeCaseJsonRenderer",
    ],
}


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
          "bucket_name": os.environ.get("AWS_STORAGE_BUCKET_NAME", ""),
          "endpoint_url": os.environ.get("AWS_S3_ENDPOINT_URL", "")
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
          "bucket_name": os.environ.get("AWS_STATIC_STORAGE_BUCKET_NAME", ""),
          "endpoint_url": os.environ.get("AWS_STATIC_S3_ENDPOINT_URL", "")
        },
    },
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=45),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}


INSTALLED_APPS = [
    "user",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_ses",
    "django_extensions",
    "django_filters",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "request",
]

AUTH_USER_MODEL = "user.User"

MIGRATION_MODULES = {
    "user": "user.model_data.migrations",
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "request.middleware.RequestMiddleware",
]

ROOT_URLCONF = "nosylos_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "nosylos_api.wsgi.application"

if "RDS_HOSTNAME" in os.environ:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.environ["RDS_DB_NAME"],
            "USER": os.environ["RDS_USERNAME"],
            "PASSWORD": os.environ["RDS_PASSWORD"],
            "HOST": os.environ["RDS_HOSTNAME"],
            "PORT": os.environ["RDS_PORT"],
        }
    }
else:
    if "TF_VAR_POSTGRES_PASSWORD" in os.environ:
        password = os.environ["TF_VAR_POSTGRES_PASSWORD"]
        host = "postgres"
    else:
        # Here set your local instance's password
        password = "localpassword"
        # checkov:skip=CKV_SECRET_80: Local password, no critical data
        host = "db"
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "test_db",
            "USER": "postgres",
            "PASSWORD": password,
            "HOST": host,
            "PORT": "5432",
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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ADMINS = [
    ("usage", "unilluminatedsages@gmail.com"),
]

SUPPORT_EMAIL = "support@nosylos.com"

if "AWS_SES_ACCESS_KEY_ID" in os.environ:
    EMAIL_BACKEND = "django_ses.SESBackend"
    AWS_SES_CONFIGURATION_SET = "support"
    AWS_SES_ACCESS_KEY_ID = os.environ["AWS_SES_ACCESS_KEY_ID"]
    AWS_SES_SECRET_ACCESS_KEY = os.environ["AWS_SES_SECRET_ACCESS_KEY"]
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

if "STRIPE_PRODUCTION_KEY_ID" in os.environ:
    STRIPE_KEY = os.environ["STRIPE_PRODUCTION_KEY_ID"]
else:
    # checkov:skip=CKV_SECRET_6: Test key can't break anything
    STRIPE_KEY = "test_key"

# django-request configs
REQUEST_ANONYMOUS_IP = True
REQUEST_IGNORE_PATHS = (r"^argolis/*",)
REQUEST_TRAFFIC_MODULES = (
    "request.traffic.UniqueVisitor",
    "request.traffic.UniqueVisit",
    "request.traffic.Hit",
    "request.traffic.Error",
)
