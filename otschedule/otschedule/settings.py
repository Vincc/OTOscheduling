from pathlib import Path
import os

"""Django GENERATED SETTINGS"""

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-ag^0k1^=j#ff5j@_o6-wfk472(nt3eose9+-slrq6(u6v&5xt!"


DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = "otrender.user"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "otrender",
    "crispy_forms",
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

ROOT_URLCONF = "otschedule.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "otschedule.wsgi.application"


# Database


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "otdata",
        "USER": "otadmin",
        "PASSWORD": "2122004",
        "HOST": "localhost",
        "PORT": "3306",
    }
}


# Password validation


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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = False                 
TIME_FORMAT = "H:i"

USE_TZ = True


# Static files (CSS, JavaScript, Images)


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# Default primary key field type


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
