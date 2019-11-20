import logging

import slack

from django.conf import settings


logger = logging.getLogger(__name__)


# bvanvugt: Wrap the slack web client in our own so we can disable it in non-prod environments.
class SlackClient:
    """ We wrap the slack web client in our own client so we can eat calls when slack is not connected. """

    def __init__(self):
        self.web_client = None
        if settings.SLACK_API_TOKEN:
            self.web_client = slack.WebClient(token=settings.SLACK_API_TOKEN, timeout=5)

    def send_message(self, text="(unknwon)"):
        if self.web_client:
            try:
                response = self.web_client.chat_postMessage(
                    as_user=False,
                    icon_emoji=":printer:",
                    username=f"battlesnake/play:{settings.APP_VERSION}",
                    channel="#play-event-log",
                    text=text,
                )
                response.validate()
            except Exception as e:
                logger.error(f"Error sending message to Slack: {e}")
