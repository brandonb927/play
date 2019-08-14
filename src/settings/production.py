from settings.base import *  # noqa


# Database Config

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

# Request handling

ALLOWED_HOSTS = [get_environment_variable("BATTLESNAKE_PLAY_HOST")]  # noqa
# Accept proxy headers
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PROTO = True
# Redirect if proxy doesn't indicate HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# Ask browsers to force HTTPS
SECURE_HSTS_SECONDS = 3600  # just 1 hour to start to make sure it works correctly
# Only accept cookies over HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

# SENTRY_KEY = get_env("SENTRY_KEY", "")
# if SENTRY_KEY:
#     sentry_sdk.init(dsn=SENTRY_KEY, integrations=[DjangoIntegration()], environment=ENV)

# SLACK_EVENTS_URL = get_env("SLACK_EVENTS_URL", "")


SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
