from datetime import timedelta
from email.policy import default
from pathlib import Path
from decouple import config
import os

import dj_database_url
from kombu import Queue, Exchange

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# Debug mode should be False in production
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts/domain names that are valid for this site
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

# CORS configuration
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', default=False, cast=bool)

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
DATABASES = {
    'default': dj_database_url.config(
        default=f"postgresql://{config('DB_USER')}:{config('DB_PASS')}@{config('DB_SERVICE_NAME')}:{config('DB_PORT')}/{config('DB_DATABASE')}",
        conn_max_age=600  # Connection persistence
    )
}

# Email configuration (default is console backend)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# Uncomment and configure the following lines to use an SMTP backend
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'your_email@example.com'
# EMAIL_HOST_PASSWORD = 'your_password'
# EMAIL_USE_TLS = True

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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'build/static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

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
    'JWT_AUTH_SECURE': False,
    'JWT_AUTH_HTTPONLY': True,
    'JWT_AUTH_SAMESITE': 'Lax',
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
GOOGLE_REDIRECT_URL = config('GOOGLE_REDIRECT_URL', default='')
GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID', default='')
GOOGLE_CLIENT_SECRET = config('GOOGLE_CLIENT_SECRET', default='')

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

# Media files configuration
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Celery Configuration Options
CELERY_TIMEZONE = "Asia/Tbilisi"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes

CELERY_BROKER_URL = 'amqp://guest:guest@rabbit:5672/'  # RabbitMQ broker URL

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'ManagerX-api': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# Example OAuth URL (for reference)
# https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://localhost:8000/accounts/google/login/callback/&prompt=consent&response_type=code&client_id=replace_me_client_id&scope=openid%20email%20profile&access_type=offline
