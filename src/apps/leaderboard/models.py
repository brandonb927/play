from django.db import models

from apps.core.models import Game, Snake
from util.models import BaseModel
from util.fields import ShortUUIDField


class GameLeaderboard(BaseModel):
    """ Tracks a game from the leaderboard perspective. """

    game = models.OneToOneField(Game, null=True, blank=True, on_delete=models.SET_NULL)
    ranked = models.BooleanField(default=False)


class SnakeLeaderboard(BaseModel):
    """ Tracks a snakes involvement in the leaderboard. """

    def __init__(self, *args, **kwargs):
        self._rank = False
        super().__init__(*args, **kwargs)

    id = ShortUUIDField(prefix="slb", max_length=128, primary_key=True)
    snake = models.ForeignKey(Snake, null=True, on_delete=models.CASCADE)
    mu = models.FloatField(null=True)
    sigma = models.FloatField(null=True)
    unhealthy_counter = models.IntegerField(null=True)

    @property
    def rank(self):
        return self.mu or 25

    @classmethod
    def ranked(cls):
        snakes = list(SnakeLeaderboard.objects.all())
        return sorted(snakes, key=lambda s: s.rank, reverse=True)

    def __str__(self):
        return f"{self.snake.name}"

    def reset_unhealthy_counter(self):
        if self.unhealthy_counter is not None and self.unhealthy_counter > 0:
            self.unhealthy_counter = 0
            self.save(update_fields=["unhealthy_counter"])

    def is_unhealthy(self):
        if self.unhealthy_counter is not None and self.unhealthy_counter > 5:
            return True
        return False

    def increase_unhealthy_counter(self):
        if self.unhealthy_counter is None:
            self.unhealthy_counter = 0
        self.unhealthy_counter += 1
        self.save(update_fields=["unhealthy_counter"])

    class Meta:
        app_label = "leaderboard"


class LeaderboardResult(BaseModel):
    snake = models.ForeignKey(SnakeLeaderboard, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    mu_change = models.FloatField()
    sigma_change = models.FloatField()
