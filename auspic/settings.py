import os
from collections import OrderedDict
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    "SECRET_KEY", default="*4cd27_pf(=$okakifzkcl8sq(xtawv&$p-2(5e(zboaem#3i!"
)

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_PLUGINS = [
    "tinymce",
    "registration",
    "crispy_forms",
    "crispy_bootstrap5",
    "easy_thumbnails",
    "django_filters",
    "import_export",
    'mptt',
]


DJANGO_APPS = [
    "admin_interface",
    "colorfield",
    "accounts",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


MODULES = [
    "web",
    
    "order",
    "main",
    "products",
]

INSTALLED_APPS = INSTALLED_PLUGINS + DJANGO_APPS + MODULES

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "auspic.urls"

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
                "web.context_processors.main_context",
            ],
        },
    },
]

WSGI_APPLICATION = "auspic.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": config("DB_NAME", default=BASE_DIR / "db.sqlite3"),
        "USER": config("DB_USER", default=""),
        "PASSWORD": config("DB_PASSWORD", default=""),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": "5432",
        "OPTIONS": {},
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    # {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

USE_L10N = False
# DATE_INPUT_FORMATS = (
#     "%d/%m/%Y",
#     "%d-%m-%Y",
#     "%d/%m/%y",
#     "%d %b %Y",
#     "%d %b, %Y",
#     "%d %b %Y",
#     "%d %b, %Y",
#     "%d %B, %Y",
#     "%d %B %Y",
# )
DATETIME_INPUT_FORMATS = (
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%d/%m/%Y",
    "%d/%m/%y %H:%M:%S",
    "%d/%m/%y %H:%M",
    "%d/%m/%y",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
)

VERSATILEIMAGEFIELD_SETTINGS = {
    "cache_length": 2592000,
    "cache_name": "versatileimagefield_cache",
    "jpeg_resize_quality": 70,
    "sized_directory_name": "__sized__",
    "filtered_directory_name": "__filtered__",
    "placeholder_directory_name": "__placeholder__",
    "create_images_on_demand": True,
    "image_key_post_processor": None,
    "progressive_jpeg": False,
}

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

THUMBNAIL_ALIASES = {
    "": {
        "small": {"size": (300, 300), "crop": True},
        "extra_small": {"size": (200, 200), "crop": True},
        "medium": {"size": (800, 1200), "crop": False},
        "banner": {"size": (1660, 430), "crop": True},
    }
}
THUMBNAIL_BASEDIR = "thumbnails"

LANGUAGE_CODE = "en-us"


TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

USE_L10N = True
# TRANSLATABLE_MODEL_MODULES = ["products"]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
STATIC_URL = "/static/"
STATIC_FILE_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = ((BASE_DIR / "static"),)
STATIC_ROOT = BASE_DIR / "assets"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True

REGISTRATION_OPEN = True
LOGIN_URL = "/accounts/login/"
LOGOUT_URL = "/accounts/logout/"
LOGIN_REDIRECT_URL = "/"

EMAIL_BACKEND = config("EMAIL_BACKEND")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

# This did the trick
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

APP_ORDER = OrderedDict(
    [
        (
            "products",
            [
                "Slider",
                "Category",
                "SubCategory",
                "Product",
                "ProductVariant",
                "ProductSpecification",
                "ProductImage",
                "Offer",
            ],
        ),
    ]
)

SESSION_COOKIE_SECURE = True  # Set to True to only send the cookie over HTTPS
SESSION_COOKIE_SAMESITE = None
DOMAIN = "https://auspic.geany.website"

RAZOR_PAY_KEY = config("RAZOR_PAY_KEY", default="12345")
RAZOR_PAY_SECRET = config("RAZOR_PAY_SECRET", default="1234")


AUTH_USER_MODEL = 'accounts.User'
