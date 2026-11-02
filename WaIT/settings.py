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

# ========== تنظیمات امنیتی ==========
<<<<<<< HEAD
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-4)d^mi5q%tf2^0nnuh+=fq8i)_!wc1=&9y_=o_*&n5a35#n7&j')

# تشخیص محیط (محلی یا سرور)
import socket
HOSTNAME = socket.gethostname()
IS_PRODUCTION = 'nowaitapp' in HOSTNAME or 'server' in HOSTNAME  # بر اساس نام سرور تنظیم کن

=======
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-4)d^mi5q%tf2^0nnuh+=fq8i)_!wc1=&9y_=o_*&n5a35#n7&j",
)

# تشخیص محیط (محلی یا سرور)
import socket

HOSTNAME = socket.gethostname()
IS_PRODUCTION = "nowaitapp" in HOSTNAME or "server" in HOSTNAME

>>>>>>> develop
# تنظیمات بر اساس محیط
if IS_PRODUCTION:
    DEBUG = False
    ALLOWED_HOSTS = [
<<<<<<< HEAD
        'nowaitapp.ir',
        'www.nowaitapp.ir',
        'api.nowaitapp.ir',
    ]
    CSRF_TRUSTED_ORIGINS = [
        'https://nowaitapp.ir',
        'https://www.nowaitapp.ir',
=======
        "nowaitapp.ir",
        "www.nowaitapp.ir",
        "api.nowaitapp.ir",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "https://nowaitapp.ir",
        "https://www.nowaitapp.ir",
>>>>>>> develop
    ]
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
<<<<<<< HEAD
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    FRONTEND_URL = "https://nowaitapp.ir"
else:
    DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
    CSRF_TRUSTED_ORIGINS = [
        'http://127.0.0.1:8000',
        'http://localhost:8000',
=======
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    FRONTEND_URL = "https://nowaitapp.ir"
else:
    DEBUG = True
    ALLOWED_HOSTS = [
        "127.0.0.1",
        "localhost",
        "192.168.1.175",
        "192.168.1.*",
        "*",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://192.168.1.175:8000",
>>>>>>> develop
    ]
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    FRONTEND_URL = "http://127.0.0.1:8000"
<<<<<<< HEAD
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
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
=======

# ==================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core.apps.CoreConfig",
    "accounts.apps.AccountsConfig",
    "rest_framework",
    "drf_yasg",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
>>>>>>> develop
]

# تنظیمات CORS
if IS_PRODUCTION:
    CORS_ALLOWED_ORIGINS = [
        "https://nowaitapp.ir",
        "https://www.nowaitapp.ir",
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
<<<<<<< HEAD
        "http://127.0.0.1:3000",  # برای React
=======
        "http://192.168.1.175:8000",
        "http://127.0.0.1:3000",
>>>>>>> develop
        "http://localhost:3000",
    ]

CORS_ALLOW_CREDENTIALS = True
<<<<<<< HEAD

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
=======
CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = "WaIT.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
>>>>>>> develop
            ],
        },
    },
]

WSGI_APPLICATION = "WaIT.wsgi.application"

# ========== دیتابیس ==========
if IS_PRODUCTION:
<<<<<<< HEAD
    # برای سرور از PostgreSQL استفاده کن
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'wait_db'),
            'USER': os.environ.get('DB_USER', 'wait_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    # برای لوکال از SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
=======
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", "wait_db"),
            "USER": os.environ.get("DB_USER", "wait_user"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

>>>>>>> develop
# ==================================================

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

<<<<<<< HEAD
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [BASE_DIR / 'staticfiles']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========== تنظیمات JWT ==========
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
=======
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

# ========== تنظیمات فایل‌های استاتیک ==========
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [BASE_DIR / "staticfiles"]

# برای اطمینان از اینکه فایل‌های استاتیک بارگذاری میشن
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ========== تنظیمات JWT ==========
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
>>>>>>> develop
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
}
<<<<<<< HEAD

AUTH_USER_MODEL = 'accounts.User'

=======

AUTH_USER_MODEL = "accounts.User"

>>>>>>> develop
# ========== تنظیمات OTP ==========
OTP_TTL_SECONDS = 300
OTP_SEND_RATE_LIMIT = 5
OTP_MAX_VERIFY_ATTEMPTS = 5
OTP_ATTEMPT_WINDOW_SECONDS = 300
QUEUE_RATING_WINDOW = timedelta(hours=12)

# ========== تنظیمات SMS ==========
<<<<<<< HEAD
GHASEDAK_API_KEY = os.environ.get('GHASEDAK_API_KEY', 'P/gEN/k+t6qVTLRd1Fzede42XCe+wJjYkGsLKx2ZaGM')
GHASEDAK_URLS = [
    "https://api.ghasedaksms.com/v2/send/verify",
    "https://rest.ghasedaksms.com/v2/send/verify",
=======
GHASEDAK_API_KEY = os.environ.get(
    "GHASEDAK_API_KEY", "P/gEN/k+t6qVTLRd1Fzede42XCe+wJjYkGsLKx2ZaGM"
)

GHASEDAK_URLS = [
    "https://api.ghasedaksms.com/v2/send/simple",
    "http://api.ghasedaksms.com/v2/send/simple",
    "https://rest.ghasedaksms.com/v2/send/simple",
    "http://rest.ghasedaksms.com/v2/send/simple",
    "https://gateway.ghasedak.me/rest/api/v1/send/simple",
    "https://gateway.ghasedak.me/api/v1/send/simple",
    "https://rest.ghasedak.me/v2/send/simple",
    "https://api.ghasedak.me/v2/send/simple",
>>>>>>> develop
]

# ========== آدرس فرانت ==========
FRONTEND_URL = "https://nowaitapp.ir" if IS_PRODUCTION else "http://127.0.0.1:8000"

# ========== لاگینگ ==========
LOGGING = {
<<<<<<< HEAD
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': str(BASE_DIR / 'logs' / 'error.log'),
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
=======
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": str(BASE_DIR / "logs" / "error.log"),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
>>>>>>> develop
