import logging

import analytics

from django.conf import settings

logger = logging.getLogger(__name__)


# chris: build a wrapper around the Segment API to handle some of the common formatting and hide the event types
class SegmentClient:
    class EVENTS:
        NEW_SNAKE = "New Snake"
        GAME_STARTED = "Game Started"
        EVENT_REGISTER = "Event Registration"
        DELETE_SNAKE = "Delete Snake"
        UPDATE_SNAKE = "Update Snake"
        SNAKE_USED = "Snake Used"
        GAME_WATCHED = "Game Watched"

    class EVENT_CATEGORIES:
        SNAKES = "Snakes"
        GAMES = "Games"
        EVENTS = "Events"

    def __init__(self):
        self.tracking_enabled = False
        if settings.SEGMENT_API_KEY:
            analytics.write_key = settings.SEGMENT_API_KEY
            self.tracking_enabled = True

    def identify(self, account):
        if self.tracking_enabled:
            try:
                # Make sure analytics tracking can't crash the triggering action
                analytics.identify(
                    account.id,
                    {"email": account.user.email, "username": account.user.username},
                )
            except Exception as e:
                logger.exception("Failed to write BI identify %s" % account, e)

    def __track(self, account, event, payload):
        if self.tracking_enabled:
            try:
                # Make sure analytics tracking can't crash the triggering action
                analytics.track(account.id, event, payload)
            except Exception as e:
                logger.exception("Failed to write BI event %s" % event, e)

    def snake_created(self, account, snake):
        self.__track(
            account,
            SegmentClient.EVENTS.NEW_SNAKE,
            {
                "category": SegmentClient.EVENT_CATEGORIES.SNAKES,
                "label": snake.name,
                "value": str(1 if snake.is_public else 0),
                "public": str(snake.is_public),
            },
        )

    def snake_deleted(self, account, snake):
        self.__track(
            account,
            SegmentClient.EVENTS.DELETE_SNAKE,
            {
                "category": SegmentClient.EVENT_CATEGORIES.SNAKES,
                "label": snake.name,
                "value": str(1 if snake.is_public else 0),
                "public": str(snake.is_public),
            },
        )

    def snake_updated(self, account, snake):
        self.__track(
            account,
            SegmentClient.EVENTS.UPDATE_SNAKE,
            {
                "category": SegmentClient.EVENT_CATEGORIES.SNAKES,
                "label": snake.name,
                "value": str(1 if snake.is_public else 0),
                "public": str(snake.is_public),
            },
        )

    def snake_used(self, account, snake, game):
        self.__track(
            account,
            SegmentClient.EVENTS.SNAKE_USED,
            {
                "category": SegmentClient.EVENT_CATEGORIES.SNAKES,
                "label": snake.name,
                "value": "1",
                "game": game.id,
            },
        )

    def game_started(self, account, game):
        self.__track(
            account,
            SegmentClient.EVENTS.GAME_STARTED,
            {
                "category": SegmentClient.EVENT_CATEGORIES.GAMES,
                "label": game.id,
                "value": "1",
                "snakes": str(game.snakes.count()),
                "boardWidth": str(game.width),
                "boardHeight": str(game.height),
                "engine": game.engine_id,
            },
        )
        for snake in game.snakes.all():
            self.snake_used(account, snake, game)

    def event_registration(self, account, event, team):
        self.__track(
            account,
            SegmentClient.EVENTS.EVENT_REGISTER,
            {
                "category": SegmentClient.EVENT_CATEGORIES.EVENTS,
                "label": event.slug,
                "value": "1",
                "team": team.name,
                "div": team.division,
            },
        )

    def game_watched(self, account, game):
        self.__track(
            account,
            SegmentClient.EVENTS.GAME_WATCHED,
            {
                "category": SegmentClient.EVENT_CATEGORIES.GAMES,
                "label": game.id,
                "value": "1",
                "snakes": str(game.snakes.count()),
                "boardWidth": str(game.width),
                "boardHeight": str(game.height),
                "engine": game.engine_id,
            },
        )


def on_segment_error(error, items):
    logger.error("An error occured with segment request: %s" % error)


analytics.on_error = on_segment_error
