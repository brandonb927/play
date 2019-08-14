from settings.base import *  # noqa: F403

import os

# Force test DB to use SQLite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),  # noqa: F405
    }
}

# Null these out to avoid hitting them in tests.
BATTLESNAKE_BOARD_HOST = ""
BATTLESNAKE_ENGINE_HOST = ""
BATTLESNAKE_EXPORTER_HOST = ""

BATTLESNAKE_BOARD_URL = ""
BATTLESNAKE_ENGINE_URL = ""
BATTLESNAKE_EXPORTER_URL = ""
