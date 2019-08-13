from settings.base import *  # noqa

import os

# bvanvugt: Temporary until it's working.

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(BASE_DIR, "db.sqlite3"),  # noqa
#     }
# }
DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_environment_variable("POSTGRES_DB"),
        "USER": get_environment_variable("POSTGRES_USER"),
        "PASSWORD": get_environment_variable("POSTGRES_PASSWORD"),
        "HOST": get_environment_variable("POSTGRES_HOST"),
        "PORT": get_environment_variable("POSTGRES_PORT"),
    }
}

# bvanvugt: Temporary until it's working.


# Request handling

ALLOWED_HOSTS = [get_environment_variable("BATTLESNAKE_PLAY_HOST")]  # noqa
# Forwarding through the proxy
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PROTO = True
# This cannot be enabled in prod because the pods are behind an SSL termination point at the ingress
# SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600  # just 1 hour to start to make sure it works correctly


# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

# SENTRY_KEY = get_env("SENTRY_KEY", "")
# if SENTRY_KEY:
#     sentry_sdk.init(dsn=SENTRY_KEY, integrations=[DjangoIntegration()], environment=ENV)

# SLACK_EVENTS_URL = get_env("SLACK_EVENTS_URL", "")


# bvanvugt: Temporary
# if is_production_env() or get_env("POSTGRES_HOST", None, True) is not None:
#     """
#     Only enable the PG config if we're running in production
#     """
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql_psycopg2",
#             "NAME": get_env("POSTGRES_DB", "battlesnakeio_play", True),
#             "USER": get_env("POSTGRES_USER", None, False),
#             "PASSWORD": get_env("POSTGRES_PASSWORD", None, False),
#             "HOST": get_env("POSTGRES_HOST", None, False),
#             "PORT": get_env("POSTGRES_PORT", None, False),
#         }
#     }

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True


# bvanvugt: Do we need this?
# if is_production_env():
#     domain = get_env("BATTLESNAKEIO_DOMAIN", "play.battlesnake.io", True)
#     STATIC_URL = f"https://{domain}/static/"
