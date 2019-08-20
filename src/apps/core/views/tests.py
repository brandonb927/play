import mock

from django.test import Client, TestCase

from apps.core.factories import GameFactory, SnakeFactory
from apps.core.models import GameSnake, Profile, Snake
from apps.authentication.factories import UserFactory


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

        snake1 = self.snake_factory.basic(n=1, commit=True, profile=self.user.profile)
        snake2 = self.snake_factory.basic(n=1, commit=True, profile=self.user.profile)

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
        snake = self.snake_factory.basic(n=1, profile=self.user.profile)
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
        profile = self.user_factory.basic(commit=True).profile
        GameSnake.objects.create(
            game=game, snake=self.snake_factory.basic(profile=profile, commit=True)
        )
        GameSnake.objects.create(
            game=game, snake=self.snake_factory.basic(profile=profile, commit=True)
        )
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(url, response.content.decode("utf-8"))


class ProfileViewsTestCase(TestCase):
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
        self.assertEqual(Profile.objects.get(user=self.user).email, "my-new-email")

    def test_update_no_email(self):
        response = self.client.post("/settings/", {"email": "", "_method": "PUT"})
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        response = self.client.delete("/settings/")
        self.assertEqual(response.status_code, 302)

    def test_get(self):
        response = self.client.get(f"/u/{self.user.username}/")
        self.assertEqual(response.status_code, 200)

    def test_get_case_insensitive(self):
        response = self.client.get(f"/u/{self.user.username.upper()}/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/u/{self.user.username}/")

    def test_snakes_are_returned_in_response(self):
        Snake.objects.create(
            profile=self.user.profile, account=self.user.account, name="My Snake"
        )
        response = self.client.get(f"/u/{self.user.username}/")
        self.assertEqual(
            response.context[-1]["profile"].user.profile.snakes[0].name, "My Snake"
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

        snakes = Snake.objects.filter(profile=self.user.profile)
        self.assertEqual(snakes.count(), 1)

        snake = snakes.first()
        self.assertEqual(snake.name, "My Snake")
        self.assertEqual(snake.url, "https://dedsnek.herokuapp.com")
        self.assertIsNotNone(snake.profile)

    def test_get(self):
        snake = Snake.objects.create(
            profile=self.user.profile, account=self.user.account, name="My Snake"
        )
        response = self.client.get(f"/s/{snake.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]["snake"], snake)

    def test_edit(self):
        snake = Snake.objects.create(
            profile=self.user.profile, account=self.user.account, name="My Snake"
        )
        response = self.client.get(f"/s/{snake.id}/edit/")
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        snake = Snake.objects.create(
            profile=self.user.profile, account=self.user.account, name="My Snake"
        )
        response = self.client.post(
            f"/s/{snake.id}/edit/",
            {"name": "updated-name", "url": "updated-url", "_method": "PUT"},
        )
        self.assertEqual(response.status_code, 302)

        snake.refresh_from_db()
        self.assertEqual(snake.name, "updated-name")
        self.assertEqual(snake.url, "updated-url")
