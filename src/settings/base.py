"""
Django settings for play project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys

import django.contrib.messages as messages


def get_environment_variable(key, default=None):
    if key in os.environ:
        return os.environ[key]
    if default is None:
        raise NotImplementedError("Environment variable is unset: '%s'" % key)
    return default


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_environment_variable("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# These should be configured in environment-specific settings
ALLOWED_HOSTS = []
DATABASES = None


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "social_django",
    "widget_tweaks",
    "apps.authentication",
    "apps.jobs",
    "apps.core",
    "apps.event",
    "apps.leaderboard",
    "apps.ui",
    "apps.staff",
]

ROOT_URLCONF = "urls"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [(os.path.join(BASE_DIR, "templates"))],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "apps.common.context_processors.common",
            ],
            "builtins": [
                "django.contrib.staticfiles.templatetags.staticfiles",
                "apps.ui.templatetags.markdown",
            ],
        },
    }
]


WSGI_APPLICATION = "wsgi.application"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

APPEND_SLASH = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(message)s"},
        "standard": {"format": "[%(process)d] [%(levelname)s] %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "standard",
        }
    },
    "loggers": {
        "console": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        # Route all logs to console by default.
        "apps": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        "settings": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        # Library loggers
        "gunicorn": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "requests": {"handlers": ["console"], "level": "WARNING", "propagate": False},
    },
}

# -----------------------------------------------------------------------------
# Everything past this point is specific to us.
# -----------------------------------------------------------------------------

# This is not important, strictly for display. Grab it if available.
APP_VERSION = get_environment_variable("APP_VERSION", "0.0.0")

MAINTENANCE_MODE = bool(
    get_environment_variable("DJANGO_MAINTENANCE_MODE", "false") == "true"
)


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "authentication.User"

# bvanvugt: Right now we only support GitHub OAuth, disable everything else.
AUTHENTICATION_BACKENDS = (
    "social_core.backends.github.GithubOAuth2",
    # "django.contrib.auth.backends.ModelBackend",
)
AUTH_PASSWORD_VALIDATORS = [
    # {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    # {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    # {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    # {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Set these in environment specific settings
SOCIAL_AUTH_GITHUB_KEY = None
SOCIAL_AUTH_GITHUB_SECRET = None

SOCIAL_AUTH_GITHUB_SCOPE = ["user:email"]

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "apps.authentication.pipeline.blacklist_usernames",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "apps.authentication.pipeline.create_account",
)

# These are used heavily by Django and Django Social Auth
LOGIN_URL = "login"
LOGOUT_URL = "logout"
LOGIN_REDIRECT_URL = "home"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "apps/ui/static")]


# Silencing system checks that are unneeded.
# https://docs.djangoproject.com/en/2.1/ref/checks/
SILENCED_SYSTEM_CHECKS = ["fields.W342"]


# Bootstrap alert messaging
MESSAGE_TAGS = {
    messages.constants.DEBUG: "alert-info",
    messages.constants.INFO: "alert-info",
    messages.constants.SUCCESS: "alert-success",
    messages.constants.WARNING: "alert-warning",
    messages.constants.ERROR: "alert-danger",
}

# Configure other battlesnake services

BATTLESNAKE_BOARD_HOST = get_environment_variable(
    "BATTLESNAKE_BOARD_HOST", "board.battlesnake.com"
)
BATTLESNAKE_ENGINE_HOST = get_environment_variable(
    "BATTLESNAKE_ENGINE_HOST", "engine.battlesnake.com"
)
BATTLESNAKE_EXPORTER_HOST = get_environment_variable(
    "BATTLESNAKE_EXPORTER_HOST", "exporter.battlesnake.com"
)

BATTLESNAKE_BOARD_URL = "https://{}".format(BATTLESNAKE_BOARD_HOST)
BATTLESNAKE_ENGINE_URL = "https://{}".format(BATTLESNAKE_ENGINE_HOST)
BATTLESNAKE_EXPORTER_URL = "https://{}".format(BATTLESNAKE_EXPORTER_HOST)

# Slack Service
SLACK_API_TOKEN = None

# Google Analytics
GOOGLE_ANALYTICS_ID = None
