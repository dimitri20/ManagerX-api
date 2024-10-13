from datetime import timedelta
from email.policy import default
from pathlib import Path
import os

import os

from pathlib import Path
from . import is_true, split_with_comma

import dj_database_url
from kombu import Queue, Exchange

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

INSECURE_KEY = "django-insecure-0eikswwglid=ukts4l2_b=676m!-q_%154%2z@&l3)n6)cp3#c"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", INSECURE_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = is_true(os.getenv("DJANGO_DEBUG", "true"))

CORS_ALLOWED_ORIGINS = split_with_comma(
    os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:8080")
)
CORS_ALLOW_CREDENTIALS = is_true(os.getenv("CORS_ALLOW_CREDENTIALS", 'true'))
CORS_ALLOW_METHODS = split_with_comma(os.getenv("CORS_ALLOW_METHODS"))
CORS_ALLOW_HEADERS = split_with_comma(os.getenv("CORS_ALLOW_HEADERS"))

# Hosts/domain names that are valid for this site
ALLOWED_HOSTS = split_with_comma(
    os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost")
)

INTERNAL_IPS = ["127.0.0.1"]

if DEBUG:
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#configure-internal-ips
    import socket

    try:
        hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
        INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]
    except socket.gaierror:
        INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]


# CORS configuration
# CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
# CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', default=False, cast=bool)

# Application definition
DJANGO_DEFAULT_APPS = [
    'daphne',  # for ASGI support
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'corsheaders',
    'django_filters',
    'django_mailbox',
    'drf_yasg',  # Swagger documentation
]

CUSTOM_APPS = [
    'apps.accounts',
    'apps.tasks',
    'apps.expertiseMainFlow',
    'apps.notifications',
]

# Combined list of installed apps
INSTALLED_APPS = DJANGO_DEFAULT_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

# Site framework
SITE_ID = 1  # Required for django.contrib.sites

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default authentication
    'allauth.account.auth_backends.AuthenticationBackend',  # Django Allauth backend
]

# Middleware configuration
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS headers for cross-origin requests
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files in production
    'allauth.account.middleware.AccountMiddleware',  # Allauth middleware
]

# URL configuration
ROOT_URLCONF = 'ManagerX-api.urls'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'build')],  # Custom template directory
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

# ASGI application (for Channels)
ASGI_APPLICATION = "ManagerX-api.asgi.application"

# Channel layers configuration (for Django Channels)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],  # Redis server details
        },
    },
}

# Database configuration
# DATABASES = {
#     'default': dj_database_url.config(
#         default=f"postgresql://{config('DB_USER')}:{config('DB_PASS')}@{config('DB_SERVICE_NAME')}:{config('DB_PORT')}/{config('DB_DATABASE')}",
#         conn_max_age=600  # Connection persistence
#     )
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": Path(os.getenv("DJANGO_SQLITE_DIR", "")) / "db.sqlite3",
    }
}

# If POSTGRES_DB is truthy, use PostgreSQL. https://docs.python.org/3/library/stdtypes.html#truth-value-testing
if bool(os.getenv("POSTGRES_DB")):
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": os.environ["POSTGRES_PORT"],
    }


# Email configuration (default is console backend)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Custom auth user model
AUTH_USER_MODEL = 'accounts.UserAccount'

# Password validation
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

# File upload handlers
FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

# Internationalization and localization settings
LANGUAGE_CODE = os.getenv("DJANGO_LANGUAGE_CODE", "en-us")
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.getenv("DJANGO_STATIC_ROOT")

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Sessions
SESSION_COOKIE_SECURE = is_true(os.getenv("DJANGO_SESSION_COOKIE_SECURE"))

# Settings for CSRF cookie.
CSRF_COOKIE_SECURE = is_true(os.getenv("DJANGO_CSRF_COOKIE_SECURE"))
CSRF_TRUSTED_ORIGINS = split_with_comma(os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", ""))

# Security Middleware (manage.py check --deploy)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 2  # 2 weeks, default - 0
SECURE_SSL_REDIRECT = is_true(os.getenv("DJANGO_SECURE_SSL_REDIRECT"))
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Email settings
EMAIL_HOST = os.getenv("DJANGO_EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.getenv("DJANGO_EMAIL_PORT", 25))
EMAIL_HOST_USER = os.getenv("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("DJANGO_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = is_true(os.getenv("DJANGO_EMAIL_USE_TLS"))

# Email address that error messages come from.
SERVER_EMAIL = os.getenv("DJANGO_SERVER_EMAIL", "root@localhost")

# Default email address to use for various automated correspondence from the site managers.
DEFAULT_FROM_EMAIL = os.getenv("DJANGO_DEFAULT_FROM_EMAIL", "webmaster@localhost")

# People who get code error notifications. In the format
# [('Full Name', 'email@example.com'), ('Full Name', 'anotheremail@example.com')]
ADMIN_NAME = os.getenv("DJANGO_ADMIN_NAME", "")
ADMIN_EMAIL = os.getenv("DJANGO_ADMIN_EMAIL")
if ADMIN_EMAIL:
    ADMINS = [(ADMIN_NAME, ADMIN_EMAIL)]



# Django REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
}

# dj-rest-auth configuration
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'JWT-Access',
    'JWT_AUTH_REFRESH_COOKIE': 'JWT-Refresh',
    'JWT_AUTH_REFRESH_COOKIE_PATH': '/',
    'JWT_AUTH_SECURE': True,
    'JWT_AUTH_HTTPONLY': True,
    'JWT_AUTH_SAMESITE': 'None',
    'JWT_AUTH_RETURN_EXPIRATION': False,
    'JWT_AUTH_COOKIE_USE_CSRF': False,
    'JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED': False,
    'USER_DETAILS_SERIALIZER': 'apps.accounts.serializers.CustomUserDetailsSerializer',
}

# simplejwt configuration
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# Django Allauth configuration
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
GOOGLE_REDIRECT_URL = os.getenv('GOOGLE_REDIRECT_URL', default='')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', default='')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', default='')
SOCIALACCOUNT_STORE_TOKENS = True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": GOOGLE_CLIENT_ID,  # replace with your Google client ID
            "secret": GOOGLE_CLIENT_SECRET,        # replace with your Google secret
            "key": "",                            # leave empty
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "VERIFIED_EMAIL": True,
    },
}

# Swagger (drf-yasg) configuration
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,  # Disables session-based authentication in favor of token-based authentication
    'SECURITY_DEFINITIONS': {
        'Bearer': {  # Common convention is to use "Bearer" instead of "JWT"
            'type': 'apiKey',  # Specifies that the authentication type is API key-based
            'in': 'header',  # Indicates that the token will be passed in the HTTP headers
            'name': 'Authorization',  # Defines the header name expected by the API
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"',
        }
    },
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.getenv("DJANGO_MEDIA_ROOT", "")

# URL that handles the media served from MEDIA_ROOT.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = os.getenv("DJANGO_MEDIA_URL", "media/")

GDRIVE_UPLOADS_PATH = f'{MEDIA_ROOT}/mnt/gdrive/gdrive_0'


RCLONE_USER = os.getenv("RCLONE_USER")
RCLONE_PASS = os.getenv("RCLONE_PASS")
RCLONE_ADDR = os.getenv("RCLONE_ADDR")

# Celery Configuration Options
CELERY_TIMEZONE = "Asia/Tbilisi"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes

CELERY_BROKER_URL = 'amqp://guest:guest@rabbit:5672/'  # RabbitMQ broker URL

# Log settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            # https://docs.python.org/3/library/logging.html#logrecord-attributes
            "format": "{levelname} [{asctime}] -- {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["mail_admins", "console"] if not DEBUG else ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
