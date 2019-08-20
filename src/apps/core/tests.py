import uuid
import mock

from django.test import TestCase

from apps.authentication.factories import UserFactory
from apps.core.models import Game, GameSnake
from apps.core.factories import GameFactory, SnakeFactory
from apps.core.jobs import GameStatus


class GameStatusJobTestCase(TestCase):
    def setUp(self):
        self.game_factory = GameFactory()
        self.snake_factory = SnakeFactory()
        self.user_factory = UserFactory()

    @mock.patch("apps.core.engine.status")
    @mock.patch("apps.core.engine.create")
    def test_game_status_job(self, create_mock, status_mock):
        create_mock.return_value = str(uuid.uuid4())
        game = self.game_factory.basic()
        game.save()
        snakes = self.snake_factory.basic(
            n=8, commit=True, account=self.user_factory.basic(commit=True).account
        )

        game.engine_id = str(uuid.uuid4())
        for s in snakes:
            game.snakes.add(s)
            GameSnake.objects.create(game=game, snake=s)
        game.create()
        game_snakes = GameSnake.objects.filter(game_id=game.id)

        status_mock.return_value = {
            "status": "running",
            "turn": 10,
            "snakes": {snake.id: {"death": "starvation"} for snake in game_snakes},
        }

        GameStatus().run()

        game = Game.objects.get(id=game.id)

        self.assertEqual(game.status, "running")
        self.assertEqual(game.turn, 10)
