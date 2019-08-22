import logging
import requests
from urllib.parse import urljoin

from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models, transaction
from django.db.models import Q
from django.utils.http import urlquote

from apps.common.fields import ShortUUIDField
from apps.common.models import BaseModel

from . import engine


logger = logging.getLogger(__name__)


class AccountManager(models.Manager):
    def create_for_user(self, user):
        return self.get_or_create(user=user)


class Account(BaseModel):
    id = ShortUUIDField(prefix="act", max_length=128, primary_key=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    marketing_optin = models.BooleanField(default=True, null=False)

    objects = AccountManager()

    def __str__(self):
        return f"Account[{self.id}]"


class SnakeQuerySet(models.QuerySet):
    def can_view(self, user):
        filter_query = Q(is_public=True)
        if not user.is_anonymous:
            filter_query |= Q(account=user.account)
        return self.filter(filter_query)

    def by_public_name(self, name):
        if "/" in name:
            username, snake_name = name.split("/")
            return self.filter(
                Q(account__user__username__icontains=username)
                | Q(name__icontains=snake_name)
            )
        else:
            return self.filter(
                Q(account__user__username__icontains=name) | Q(name__icontains=name)
            )


class SnakeManager(models.Manager):
    def get_queryset(self):
        return SnakeQuerySet(self.model, using=self._db)

    def can_view(self, user):
        return self.get_queryset().can_view(user)

    def by_public_name(self, name):
        return self.get_queryset().by_public_name(name)


class Snake(BaseModel):
    objects = SnakeManager()

    id = ShortUUIDField(prefix="snk", max_length=128, primary_key=True)

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="snakes"
    )

    name = models.CharField(
        max_length=128, validators=[MinLengthValidator(3), MaxLengthValidator(50)]
    )
    url = models.CharField(max_length=128)
    is_public = models.BooleanField(
        default=False, verbose_name="Allow anyone to add this snake to a game"
    )

    healthy = models.BooleanField(
        default=False, verbose_name="Did this snake respond to /ping"
    )

    @property
    def public_name(self):
        return f"{self.account.user.username} / {self.name}"

    def update_healthy(self):
        url = str(self.url)
        if not url.endswith("/"):
            url = url + "/"
        ping_url = urljoin(url, "ping")
        self.healthy = False
        try:
            status_code = self.make_ping_request(ping_url)
            if status_code == 200:
                self.healthy = True
        except Exception as e:
            logger.warning(f'Failed to ping "{self}": {e}')

        self.save(update_fields=["healthy"])

    def __str__(self):
        return f"{self.public_name}"

    def make_ping_request(self, ping_url):
        response = requests.post(ping_url, timeout=1, verify=False)
        status_code = response.status_code
        return status_code

    @property
    def games(self):
        return self.game_set.all()


class GameQuerySet(models.QuerySet):
    def watchable(self):
        return self.filter(
            status__in=(
                Game.Status.CREATED,
                Game.Status.RUNNING,
                Game.Status.STOPPED,
                Game.Status.COMPLETE,
            )
        ).exclude(engine_url__icontains="engine.internal.battlesnake.io")


class Game(BaseModel):
    """
    Game tracks a game started on the engine locally in the snake database. You
    can initialize a game through this model and call run() to start the game.
    Then, you can also call update_from_engine() at any point to refresh the
    game state from the engine onto this model.

    Creating a game looks like:

        game = Game(...) # instance created with config, ready to go
        game.create()    # game snakes created, and any other future pre-game things
        game.run()       # (OPTIONAL) sent to engine, and now it's running!
    """

    class NotCreatedError(Exception):
        pass

    class Status:
        PENDING = "pending"
        CREATED = "created"
        RUNNING = "running"
        ERROR = "error"
        STOPPED = "stopped"
        COMPLETE = "complete"

    id = ShortUUIDField(prefix="gam", max_length=128, primary_key=True)
    engine_id = models.CharField(null=True, max_length=128)
    status = models.CharField(default=Status.PENDING, max_length=30)
    turn = models.IntegerField(default=0)
    width = models.IntegerField()
    height = models.IntegerField()
    max_turns_to_next_food_spawn = models.IntegerField(default=15)
    snakes = models.ManyToManyField(Snake)
    engine_url = models.CharField(null=True, max_length=128)

    objects = GameQuerySet.as_manager()

    def config(self):
        """ Fetch the engine configuration. """
        config = {
            "width": self.width,
            "height": self.height,
            "maxTurnsToNextFoodSpawn": self.max_turns_to_next_food_spawn,
            "food": self.snakes.count(),
            "snakeTimeout": 500,
            "snakes": [
                {
                    "name": gs.name if len(gs.name) > 0 else gs.snake.public_name,
                    "url": gs.snake.url,
                    "id": gs.id,
                }
                for gs in self.gamesnake_set.all()
            ],
        }
        return config

    @transaction.atomic
    def create(self):
        """ Call the engine to create the game. Returns the game id. """
        config = self.config()
        self.engine_id = engine.create(config, self.engine_url)
        self.status = Game.Status.CREATED
        self.save()
        return self.engine_id

    def run(self):
        """ Call the engine to start the game. Returns the game id. """
        engine.run(self.engine_id, self.engine_url)
        return self.engine_id

    def engine_status(self):
        return engine.status(self.engine_id, self.engine_url)

    def update_from_engine(self):
        """ Update the status and snake statuses from the engine. """
        if self.engine_id is None:
            raise self.NotCreatedError("Game is not created")
        with transaction.atomic():
            status = engine.status(self.engine_id, self.engine_url)
            self.status = status["status"]
            self.turn = status["turn"]

            for game_snake in self.gamesnake_set.all():
                snake_status = status["snakes"][game_snake.id]
                game_snake.death = snake_status["death"]
                game_snake.save()

            self.save()
            return status

    @property
    def game_snakes(self):
        return self.gamesnake_set.all()

    def alive_game_snakes(self):
        return self.game_snakes.filter(death="pending")

    def winner(self):
        if self.status == self.Status.COMPLETE:
            living_snakes = self.alive_game_snakes()
            if living_snakes.count() == 1:
                return living_snakes.first()

    def get_board_url(self):
        engine_url = settings.BATTLESNAKE_ENGINE_URL
        if self.engine_url is not None and len(self.engine_url) > 0:
            engine_url = self.engine_url

        return f"{settings.BATTLESNAKE_BOARD_URL}/?engine={urlquote(engine_url)}&game={self.engine_id}"

    def get_gif_url(self):
        return f"{settings.BATTLESNAKE_EXPORTER_URL}/games/{self.engine_id}/gif"


class GameSnake(BaseModel):
    id = ShortUUIDField(prefix="gs", max_length=128, primary_key=True)
    snake = models.ForeignKey(Snake, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    death = models.CharField(default="pending", max_length=128)
    turns = models.IntegerField(default=0)
    name = models.CharField(default="", max_length=128)
