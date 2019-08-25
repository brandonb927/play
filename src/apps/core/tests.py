import mock

from django.test import TestCase

from .factories import GameFactory, SnakeFactory, UserFactory
from .jobs import GameStatus
from .models import Game, GameSnake


class GameStatusJobTestCase(TestCase):
    def setUp(self):
        self.game_factory = GameFactory()
        self.snake_factory = SnakeFactory()
        self.user_factory = UserFactory()

    @mock.patch("apps.core.engine.status")
    @mock.patch("apps.core.engine.create")
    def test_game_status_job(self, create_mock, status_mock):
        create_mock.return_value = "fake-engine-id-one"
        game = self.game_factory.basic()
        game.save()
        snakes = self.snake_factory.basic(
            n=8, commit=True, account=self.user_factory.basic(commit=True).account
        )

        game.engine_id = "fake-engine-id-two"
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


class GameModelTestCase(TestCase):
    def setUp(self):
        self.snake_factory = SnakeFactory()
        self.game_factory = GameFactory()
        self.user_factory = UserFactory()

    @mock.patch("apps.core.engine.create")
    def test_game_engine_configuration(self, create_mock):
        create_mock.return_value = "fake-engine-id"
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
        create_mock.return_value = "fake-engine-id"

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
        create_mock.return_value = "fake-engine-id"
        game = self.game_factory.basic()
        game.save()
        snakes = self.snake_factory.basic(
            n=8, commit=True, account=self.user_factory.basic(commit=True).account
        )

        game.engine_id = "fake-engine-id"
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


# class SnakeViewsTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user_factory = UserFactory()

#         self.user = self.user_factory.login_as(self.client)

#     def test_get(self):
#         snake = Snake.objects.create(account=self.user.account, name="My Snake")
#         response = self.client.get(f"/s/{snake.id}/")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.context[-1]["snake"], snake)

#     def test_edit(self):
#         snake = Snake.objects.create(account=self.user.account, name="My Snake")
#         response = self.client.get(f"/s/{snake.id}/edit/")
#         self.assertEqual(response.status_code, 200)

#     def test_update(self):
#         snake = Snake.objects.create(account=self.user.account, name="My Snake")
#         response = self.client.post(
#             f"/s/{snake.id}/edit/",
#             {"name": "updated-name", "url": "updated-url", "_method": "PUT"},
#         )
#         self.assertEqual(response.status_code, 302)

#         snake.refresh_from_db()
#         self.assertEqual(snake.name, "updated-name")
#         self.assertEqual(snake.url, "updated-url")
