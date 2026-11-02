"""
Django settings for WaIT project.
"""
from datetime import timedelta
from pathlib import Path
import environ
import os

env = environ.Env()
environ.Env.read_env()
BASE_DIR = Path(__file__).resolve().parent.parent

# ========== تنظیمات امنیتی برای production ==========
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-4)d^mi5q%tf2^0nnuh+=fq8i)_!wc1=&9y_=o_*&n5a35#n7&j')

# دیباگ رو خاموش کن
DEBUG = False

# دامنه‌های مجاز
ALLOWED_HOSTS = [
    'nowaitapp.ir',
    'www.nowaitapp.ir',
    'api.nowaitapp.ir',  # اگه subdomain داری
    '127.0.0.1',
    'localhost'
]

# امنیت بیشتر
CSRF_TRUSTED_ORIGINS = [
    'https://nowaitapp.ir',
    'https://www.nowaitapp.ir',
    'https://api.nowaitapp.ir'
]

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# ==================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'accounts.apps.AccountsConfig',
    'rest_framework',
    'drf_yasg',
    'corsheaders',  # برای CORS
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# تنظیمات CORS برای فرانت
CORS_ALLOWED_ORIGINS = [
    "https://nowaitapp.ir",
    "https://www.nowaitapp.ir",
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'WaIT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'WaIT.wsgi.application'

# ========== دیتابیس (SQLite برای شروع - بعداً به PostgreSQL تغییر بده) ==========
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# ==================================================

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tehran'  # تغییر به وقت تهران
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [BASE_DIR / 'staticfiles']  # برای فایل‌های استاتیک اضافی

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========== تنظیمات JWT ==========
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # برای امنیت کمتر کن
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

AUTH_USER_MODEL = 'accounts.User'

# ========== تنظیمات OTP ==========
OTP_TTL_SECONDS = 300
OTP_SEND_RATE_LIMIT = 5
OTP_MAX_VERIFY_ATTEMPTS = 5
OTP_ATTEMPT_WINDOW_SECONDS = 300
QUEUE_RATING_WINDOW = timedelta(hours=12)

# ========== تنظیمات SMS ==========
GHASEDAK_API_KEY = os.environ.get('GHASEDAK_API_KEY', 'P/gEN/k+t6qVTLRd1Fzede42XCe+wJjYkGsLKx2ZaGM')
GHASEDAK_URLS = [
    "https://api.ghasedaksms.com/v2/send/verify",
    "https://rest.ghasedaksms.com/v2/send/verify",
]

# ========== آدرس فرانت ==========
FRONTEND_URL = "https://nowaitapp.ir"

# ========== لاگینگ ==========
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}