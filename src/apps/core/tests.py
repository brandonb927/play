import mock

from django.test import Client, TestCase

from .factories import GameFactory, SnakeFactory, UserFactory
from .forms import GameForm, SnakeForm
from .jobs import GameStatus
from .models import Account, Game, GameSnake, Snake


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


class GameFormTestCase(TestCase):
    def setUp(self):
        self.snake_factory = SnakeFactory()
        self.user_factory = UserFactory()

    def test_game_form_save(self):
        user = self.user_factory.basic(commit=True)
        snake = self.snake_factory.basic(n=1, commit=True, account=user.account)

        form = GameForm(
            {"width": 10, "height": 10, "board_size": "custom", "snakes": snake.id}
        )

        self.assertTrue(form.is_valid())
        self.assertIsInstance(form.save(user), Game)

    def test_game_form_hidden_snake(self):
        user = self.user_factory.basic(commit=True)
        snake = self.snake_factory.basic(n=1, commit=True, account=user.account)

        form = GameForm(
            {"width": 10, "height": 10, "board_size": "custom", "snakes": snake.id}
        )

        self.assertTrue(form.is_valid())
        with self.assertRaises(Snake.DoesNotExist):
            form.save(
                self.user_factory.basic(email="other@test.com", commit=True)
            ), Game


class SnakeFormTestCase(TestCase):
    def setUp(self):
        self.user_factory = UserFactory()

    def test_new_snake(self):
        user = self.user_factory.basic(commit=True)
        form = SnakeForm(
            user.account,
            {"name": "DSnek", "url": "https://dsnek.herokuapp.com", "is_public": True},
        )
        form.save()
        user.refresh_from_db()
        snake = user.account.snakes.get(name="DSnek")

        self.assertEqual(snake.url, "https://dsnek.herokuapp.com")
        self.assertTrue(snake.is_public)

    def test_update_existing_snake(self):
        user = self.user_factory.basic(commit=True)
        snake = Snake.objects.create(account=user.account, name="DSnek")

        self.assertEqual(snake.url, "")
        self.assertFalse(snake.is_public)

        form = SnakeForm(
            user.account,
            {"name": "DSnek", "url": "https://dsnek.herokuapp.com", "is_public": True},
            instance=snake,
        )

        form.save()
        user.refresh_from_db()
        snake = user.account.snakes.get(name="DSnek")

        self.assertEqual(snake.url, "https://dsnek.herokuapp.com")
        self.assertTrue(snake.is_public)

    def test_new_snake_with_name_collision(self):
        user = self.user_factory.basic(commit=True)
        Snake.objects.create(account=user.account, name="DSnek")
        form = SnakeForm(
            user.account,
            {"name": "DSnek", "url": "https://dsnek.herokuapp.com", "is_public": True},
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_update_snake_with_name_collision(self):
        user = self.user_factory.basic(commit=True)
        Snake.objects.create(account=user.account, name="DSnek")
        snake = Snake.objects.create(account=user.account, name="DSnek1")

        form = SnakeForm(
            user.account,
            {"name": "DSnek", "url": "https://dsnek.herokuapp.com", "is_public": True},
            instance=snake,
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


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


class GameViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.game_factory = GameFactory()
        self.snake_factory = SnakeFactory()
        self.user_factory = UserFactory()

        self.user = self.user_factory.login_as(self.client)

    def test_new(self):
        response = self.client.get("/g/new/")
        self.assertEqual(response.status_code, 200)

    @mock.patch("apps.core.engine.run")
    @mock.patch("apps.core.engine.create")
    def test_create(self, create_mock, run_mock):
        create_mock.return_value = "a879f127-55c2-4b0c-99c9-bce09c9fc0cf"

        snake1 = self.snake_factory.basic(n=1, commit=True, account=self.user.account)
        snake2 = self.snake_factory.basic(n=1, commit=True, account=self.user.account)

        response = self.client.post(
            "/g/new/", {"board_size": "medium", "snakes": f"{snake1.id},{snake2.id}"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(create_mock.call_args_list), 1)
        self.assertEqual(len(run_mock.call_args_list), 1)

    def test_show(self):
        engine_id = "a879f127-55c2-4b0c-99c9-bce09c9fc0cf"
        url = "game=" + engine_id

        self.game_factory.basic(engine_id=engine_id, commit=True)

        response = self.client.get(f"/g/{engine_id}/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(url, response.content.decode("utf-8"))

    def test_snake_autocomplete(self):
        snake = self.snake_factory.basic(n=1, account=self.user.account)
        snake.name = "snaker"
        snake.save()

        response = self.client.get(f"/g/snake-autocomplete/?q={self.user.username}")
        j = response.json()

        self.assertEqual(len(j), 1)
        self.assertEqual(j[0]["text"], f"{self.user.username} / {snake.name}")

        response = self.client.get(f"/g/snake-autocomplete/?q={snake.name}")
        j = response.json()

        self.assertEqual(len(j), 1)
        self.assertEqual(j[0]["text"], f"{self.user.username} / {snake.name}")


class HomeViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.game_factory = GameFactory()
        self.snake_factory = SnakeFactory()
        self.user_factory = UserFactory()

    def test_home(self):
        engine_id = "a879f127-55c2-4b0c-99c9-bce09c9fc0cf"
        url = "game=" + engine_id

        games = self.game_factory.basic(
            n=20, engine_id=engine_id, status="complete", turn=200, commit=True
        )
        game = games[0]
        account = self.user_factory.basic(commit=True).account
        GameSnake.objects.create(
            game=game, snake=self.snake_factory.basic(account=account, commit=True)
        )
        GameSnake.objects.create(
            game=game, snake=self.snake_factory.basic(account=account, commit=True)
        )
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(url, response.content.decode("utf-8"))


class AccountViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_factory = UserFactory()

        self.user = self.user_factory.login_as(self.client)

    def test_edit(self):
        response = self.client.get("/settings/")
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        response = self.client.post(
            "/settings/", {"email": "my-new-email", "_method": "PUT"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Account.objects.get(user=self.user).user.email, "my-new-email")

    def test_update_no_email(self):
        response = self.client.post("/settings/", {"email": "", "_method": "PUT"})
        self.assertEqual(response.status_code, 400)

    def test_get(self):
        response = self.client.get(f"/u/{self.user.username}/")
        self.assertEqual(response.status_code, 200)

    def test_get_case_insensitive(self):
        response = self.client.get(f"/u/{self.user.username.upper()}/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/u/{self.user.username}/")

    def test_snakes_are_returned_in_response(self):
        Snake.objects.create(account=self.user.account, name="My Snake")
        response = self.client.get(f"/u/{self.user.username}/")
        self.assertEqual(
            response.context[-1]["account"].user.account.snakes.all()[:1].get().name,
            "My Snake",
        )


class SnakeViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_factory = UserFactory()

        self.user = self.user_factory.login_as(self.client)

    def test_create(self):
        response = self.client.post(
            "/s/new/", {"name": "My Snake", "url": "https://dedsnek.herokuapp.com"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(f"/u/{self.user.username}", response["Location"])

        snakes = Snake.objects.filter(account=self.user.account)
        self.assertEqual(snakes.count(), 1)

        snake = snakes.first()
        self.assertEqual(snake.name, "My Snake")
        self.assertEqual(snake.url, "https://dedsnek.herokuapp.com")
        self.assertIsNotNone(snake.account)

    def test_get(self):
        snake = Snake.objects.create(account=self.user.account, name="My Snake")
        response = self.client.get(f"/s/{snake.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]["snake"], snake)

    def test_edit(self):
        snake = Snake.objects.create(account=self.user.account, name="My Snake")
        response = self.client.get(f"/s/{snake.id}/edit/")
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        snake = Snake.objects.create(account=self.user.account, name="My Snake")
        response = self.client.post(
            f"/s/{snake.id}/edit/",
            {"name": "updated-name", "url": "updated-url", "_method": "PUT"},
        )
        self.assertEqual(response.status_code, 302)

        snake.refresh_from_db()
        self.assertEqual(snake.name, "updated-name")
        self.assertEqual(snake.url, "updated-url")
