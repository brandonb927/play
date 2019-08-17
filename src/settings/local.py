from settings.base import *  # noqa

import os


DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

SOCIAL_AUTH_GITHUB_KEY = get_environment_variable("GITHUB_CLIENT_ID")
SOCIAL_AUTH_GITHUB_SECRET = get_environment_variable("GITHUB_CLIENT_SECRET")
