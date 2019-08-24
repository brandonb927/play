from settings.base import *  # noqa


import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration as SentryDjangoIntegration


# --- Request Handling ---

ALLOWED_HOSTS = [get_environment_variable("BATTLESNAKE_PLAY_HOST")]
# Accept proxy headers
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PROTO = True
# Redirect if proxy doesn't indicate HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# Ask browsers to force HTTPS
SECURE_HSTS_SECONDS = 3600  # just 1 hour to start to make sure it works correctly
# Disallow XSS
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "SAMEORIGIN"
# Only accept cookies over HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# --- Database Config ---

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


# --- Sentry Exception Handling ---

sentry_sdk.init(
    dsn=get_environment_variable("SENTRY_DSN"), integrations=[SentryDjangoIntegration()]
)

# --- Slack Messaging ---
SLACK_API_TOKEN = get_environment_variable("SLACK_API_TOKEN")


# --- Social Auth Config ---
SOCIAL_AUTH_GITHUB_KEY = get_environment_variable("GITHUB_CLIENT_ID")
SOCIAL_AUTH_GITHUB_SECRET = get_environment_variable("GITHUB_CLIENT_SECRET")

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
