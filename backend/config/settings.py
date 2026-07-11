# backend/config/settings.py
# ==============================================================================
# CORE IMPORTS
# ==============================================================================
import os
from pathlib import Path
from decouple import config
from datetime import timedelta
from dotenv import load_dotenv
import dj_database_url

# Switch to standard StaticFilesStorage to skip aggressive compression scanning
# from whitenoise.storage import CompressedManifestStaticFilesStorage

import cloudinary
import cloudinary.uploader
import cloudinary.api

# ==============================================================================
# BASE DIRECTORY
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

# ==============================================================================
# SECURITY
# ==============================================================================
SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-your-secret-key-here-change-in-production'
)

#DEBUG = config('DEBUG', default=True, cast=bool)
DEBUG = config('DEBUG', default=False, cast=bool)

# ==============================================================================
# SECURITY SETTINGS (Production)
# ==============================================================================

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SECURE_REFERRER_POLICY = "same-origin"
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# ==============================================================================
# ALLOWED HOSTS (RENDER + LOCAL + CUSTOM DOMAIN)
# ==============================================================================
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

ALLOWED_HOSTS += [
    "yohannestekle.com",
    "www.yohannestekle.com",
    "api.yohannestekle.com",
]

# ==============================================================================
# CSRF
# ==============================================================================
CSRF_TRUSTED_ORIGINS = [
    'https://profile-k2rv.onrender.com',
    'https://frontend-nine-sable-61.vercel.app',
    'http://localhost:3000',
    'http://127.0.0.1:8000',

    "https://yohannestekle.com",
    "https://www.yohannestekle.com",
    "https://yohannestekle.com",
]

# ==============================================================================
# APPLICATIONS
# ==============================================================================
INSTALLED_APPS = [
    #'modeltranslation',
    #'jazzmin',
    "django.contrib.admin",
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    
    'cloudinary_storage',
    'cloudinary',

    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',
    'drf_spectacular_sidecar',

    'api',
    'blog',
    'users',
    'django_ckeditor_5',
]

# ==============================================================================
# MIDDLEWARE
# ==============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # 👈 ADD THIS CRUCIAL LINE HERE
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Ensure your custom templates directory is listed right here:
        'DIRS': [BASE_DIR / 'templates'], 
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

WSGI_APPLICATION = 'config.wsgi.application'

# ==============================================================================
# DATABASE
# ==============================================================================
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

if "postgres" in DATABASES["default"]["ENGINE"]:
    DATABASES["default"]["OPTIONS"] = {
        "sslmode": "require",
    }

AUTH_USER_MODEL = 'users.User'

# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True    

# ==============================================================================
# STATIC / MEDIA
# ==============================================================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = []

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        #"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        #"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

#WHITENOISE_SKIP_COMPRESS_EXTENSIONS = (
#    "css",
#    "js",
#    "woff",
#    "woff2",
#    "ttf",
#    "map",
#)

#STATICFILES_FINDERS = [
#    "django.contrib.staticfiles.finders.FileSystemFinder",
#    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
#]

#WHITENOISE_SKIP_COMPRESS_EXTENSIONS = (
#   "jpg",
#   "jpeg",
#   "png",
#   "gif",
#   "webp",
#   "woff",
#   "woff2",
#   "ttf",
#   "eot",
#   "svg",
#)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# CORS
# ==============================================================================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
    "https://frontend-nine-sable-61.vercel.app",
    "https://yohannestekle.com",
    "https://www.yohannestekle.com",
]

CORS_ALLOW_CREDENTIALS = True

# ==============================================================================
# REST FRAMEWORK
# ==============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'config.throttling.SafeAnonRateThrottle',
        'config.throttling.SafeUserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# ==============================================================================
# JWT
# ==============================================================================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}

# ==============================================================================
# SENDGRID EMAIL CONFIGURATION (PRODUCTION READY)
# ==============================================================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = config("EMAIL_HOST", default="smtp.sendgrid.net")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)

EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", default=False, cast=bool)

EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="apikey")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="test_password")

DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL",
    default="contact@yohannestekle.com"
)

CONTACT_EMAIL = config(
    "CONTACT_EMAIL",
    default="yohannes.m.tekle@gmail.com"
)

EMAIL_TIMEOUT = 10

# ==============================================================================
# FRONTEND
# ==============================================================================
FRONTEND_URL = config(
    'FRONTEND_URL',
    default='http://localhost:5173'
)

# ==============================================================================
# CACHE
# ==============================================================================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# ==============================================================================
# JAZZMIN ADMIN
# ==============================================================================
JAZZMIN_SETTINGS = {
    "site_title": "Portfolio Admin",
    "site_header": "Portfolio",
    "site_brand": "Portfolio CMS",
    "welcome_sign": "Welcome to Portfolio Admin Dashboard",
    "copyright": "Portfolio",
    "search_model": ["users.User", "api.Project", "blog.BlogPost"],
    "show_sidebar": True,
    "navigation_expanded": True,
}

# ==============================================================================
# DRF SPECTACULAR
# ==============================================================================
SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Portfolio API',
    'DESCRIPTION': 'API documentation for profile, blog, and project features.',
    'VERSION': '1.0.0',
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
}

# ==============================================================================
# CELERY
# ==============================================================================
CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# Add configuration options for the CKEditor 5 build
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|', 'bold', 'italic', 'link', 'bulletedList', 
            'numberedList', 'blockQuote', 'insertTable', '|', 
            'outdent', 'indent', '|', 'sourceEditing', 'undo', 'redo'
        ],
        'height': 300,
        'width': '100%',
    }
}

cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME", default=""),
    api_key=config("CLOUDINARY_API_KEY", default=""),
    api_secret=config("CLOUDINARY_API_SECRET", default=""),
    secure=True,
)


# Explicitly declare available translation options
LANGUAGES = [
    ('en', 'English'),
    ('de', 'German'),
]
