import mock
import uuid

from django.test import TestCase

from apps.authentication.factories import UserFactory
from apps.core.factories import GameFactory, SnakeFactory
from apps.core.models import GameSnake


class GameModelTestCase(TestCase):
    def setUp(self):
        self.snake_factory = SnakeFactory()
        self.game_factory = GameFactory()
        self.user_factory = UserFactory()

    @mock.patch("apps.core.engine.create")
    def test_game_engine_configuration(self, create_mock):
        create_mock.return_value = str(uuid.uuid4())
        game = self.game_factory.basic()
        game.save()

        snakes = self.snake_factory.basic(
            n=8, commit=True, account=self.user_factory.basic(commit=True).account
        )
        for snake in snakes:
            game.snakes.add(snake)
            GameSnake.objects.create(snake=snake, game=game)
        game.create()

        config = game.config()

        self.assertEqual(config["height"], 20)
        self.assertEqual(config["width"], 20)
        self.assertEqual(config["food"], len(snakes))
        self.assertIsNotNone(config["snakes"][0]["id"])
        self.assertEqual(config["snakes"][0]["name"], "test / test")
        self.assertEqual(len(config["snakes"]), 8)

    @mock.patch("apps.core.engine.run")
    @mock.patch("apps.core.engine.create")
    def test_game_engine_call(self, create_mock, run_mock):
        create_mock.return_value = str(uuid.uuid4())

        game = self.game_factory.basic()
        game.save()

        snakes = self.snake_factory.basic(
            n=8, commit=True, account=self.user_factory.basic(commit=True).account
        )
        for snake in snakes:
            game.snakes.add(snake)
            GameSnake.objects.create(snake=snake, game=game)

        self.assertIsNone(game.engine_id)

        game.create()
        self.assertIsNotNone(game.engine_id)

        game.run()
        self.assertEqual(len(run_mock.call_args_list), 1)
        self.assertIsNotNone(game.engine_id)

    @mock.patch("apps.core.engine.status")
    @mock.patch("apps.core.engine.create")
    def test_game_engine_update(self, create_mock, status_mock):
        create_mock.return_value = str(uuid.uuid4())
        game = self.game_factory.basic()
        game.save()
        snakes = self.snake_factory.basic(
            n=8, commit=True, account=self.user_factory.basic(commit=True).account
        )

        game.engine_id = str(uuid.uuid4())
        for snake in snakes:
            game.snakes.add(snake)
            GameSnake.objects.create(snake=snake, game=game)

        game.create()
        game_snakes = GameSnake.objects.filter(game_id=game.id)

        status_mock.return_value = {
            "status": "running",
            "turn": 10,
            "snakes": {snake.id: {"death": "starvation"} for snake in game_snakes},
        }

        game.update_from_engine()

        self.assertEqual(len(status_mock.call_args_list), 1)
        self.assertEqual(game.status, "running")
        self.assertEqual(game.turn, 10)

    def test_game_create_game_snake_name_overrides_snake_name(self):
        game = self.game_factory.basic()
        game.save()
        snakes = self.snake_factory.basic(
            n=2, commit=True, account=self.user_factory.basic(commit=True).account
        )

        game.snakes.add(snakes[0])
        GameSnake.objects.create(snake=snakes[0], game=game)
        game.snakes.add(snakes[1])
        GameSnake.objects.create(snake=snakes[0], game=game, name="Not A Test")

        config = game.config()
        found = False
        for s in config["snakes"]:
            if s["name"] == "Not A Test":
                found = True

        self.assertTrue(found)
