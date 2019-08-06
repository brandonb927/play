import requests
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def format(user, title, message, color, fallback):
    return {
        "attachments": [
            {
                "fallback": fallback,
                "color": color,
                "author_name": user,
                "title": title,
                "text": message,
            }
        ]
    }


def log_event(**kwargs):
    if not settings.SLACK_EVENTS_URL:
        return

    try:
        response = requests.post(settings.SLACK_EVENTS_URL, json=format(**kwargs))
        response.raise_for_status()
    except Exception:
        logger.exception("failed to send message to slack")
