import mock

from django.conf import settings
from django.test import Client, TestCase

from apps.core.factories import GameFactory, SnakeFactory, UserFactory
from apps.core.models import Account, ContentReport, GameSnake, Snake


class HomepageViewTestCase(TestCase):
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


class AccountViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_factory = UserFactory()

        self.user = self.user_factory.basic(commit=True)

    def test_get(self):
        response = self.client.get(f"/profile/{self.user.account.profile_slug}/")

        self.assertEqual(response.status_code, 200)

    def test_get_case_insensitive(self):
        response = self.client.get(
            f"/profile/{self.user.account.profile_slug.upper()}/"
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/profile/{self.user.account.profile_slug}/")

    def test_snakes_are_returned_in_response(self):
        Snake.objects.create(account=self.user.account, name="My Snake")
        response = self.client.get(f"/profile/{self.user.account.profile_slug}/")

        self.assertEqual(
            response.context[-1]["account"].user.account.snakes.all()[:1].get().name,
            "My Snake",
        )


class GameViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.game_factory = GameFactory()

    def test_get(self):
        engine_id = "a879f127-55c2-4b0c-99c9-bce09c9fc0cf"
        self.game_factory.basic(engine_id=engine_id, commit=True)

        response = self.client.get(f"/g/{engine_id}/")

        self.assertEqual(response.status_code, 200)

    def test_get_not_found(self):
        response = self.client.get(f"/g/does-not-exist/")

        self.assertEqual(response.status_code, 404)


class GameGIFViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.game_factory = GameFactory()

    def test_get(self):
        engine_id = "a879f127-55c2-4b0c-99c9-bce09c9fc0cf"
        self.game_factory.basic(engine_id=engine_id, commit=True)

        response = self.client.get(f"/g/{engine_id}/gif/")

        self.assertEqual(response.status_code, 302)
        self.assertIn(settings.BATTLESNAKE_EXPORTER_URL, response.url)
        self.assertIn(engine_id, response.url)

    def test_get_not_found(self):
        response = self.client.get(f"/g/does-not-exist/gif/")

        self.assertEqual(response.status_code, 404)


class SnakeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_factory = UserFactory()

        self.user = self.user_factory.basic(commit=True)

    def test_get(self):
        snake = Snake.objects.create(account=self.user.account, name="Test Snake")
        response = self.client.get(f"/s/{snake.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]["snake"], snake)


class CreateContentReportView(TestCase):
    def setUp(self):
        self.client = Client()

        self.game_factory = GameFactory()
        self.snake_factory = SnakeFactory()
        self.user_factory = UserFactory()

    def test_anonymous(self):
        response = self.client.get("/account/report/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/account/report/")

        response = self.client.post("/account/report/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/account/report/")

    def test_get_not_allowed(self):
        self.user_factory.login_as(self.client)
        response = self.client.get("/account/report/")

        self.assertEqual(response.status_code, 405)

    def test_post(self):
        self.user_factory.login_as(self.client)
        self.assertEqual(ContentReport.objects.all().count(), 0)

        response = self.client.post(
            "/account/report/",
            {
                "report_url": "/asdf/qwer/",
                "report_content": "something is being reported here!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/asdf/qwer/")
        self.assertEqual(ContentReport.objects.all().count(), 1)

        report = ContentReport.objects.get()
        self.assertEqual(report.url, "/asdf/qwer/")
        self.assertEqual(report.text, "something is being reported here!")


class CreateGameViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.game_factory = GameFactory()
        self.snake_factory = SnakeFactory()
        self.user_factory = UserFactory()

    def test_anonymous(self):
        response = self.client.get("/account/games/create/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/account/games/create/")

    def test_get(self):
        self.user_factory.login_as(self.client)
        response = self.client.get("/account/games/create/")

        self.assertEqual(response.status_code, 200)

    @mock.patch("apps.core.engine.run")
    @mock.patch("apps.core.engine.create")
    def test_post(self, create_mock, run_mock):
        create_mock.return_value = "a879f127-55c2-4b0c-99c9-bce09c9fc0cf"

        user = self.user_factory.login_as(self.client)
        snake1 = self.snake_factory.basic(n=1, commit=True, account=user.account)
        snake2 = self.snake_factory.basic(n=1, commit=True, account=user.account)

        form_data = {"board_size": "medium", "snakes": f"{snake1.id},{snake2.id}"}
        response = self.client.post("/account/games/create/", form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/g/{create_mock.return_value}")
        self.assertEqual(len(create_mock.call_args_list), 1)
        self.assertEqual(len(run_mock.call_args_list), 1)


class CreateGameJSONHelpersViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.game_factory = GameFactory()
        self.snake_factory = SnakeFactory()
        self.user_factory = UserFactory()

    def test_anonymous(self):
        response = self.client.get("/account/games/create/json/example-helper-func/")
        self.assertEqual(response.status_code, 403)

    def test_get_random_snakes_no_snakes(self):
        self.user_factory.login_as(self.client)
        response = self.client.get("/account/games/create/json/random-snake/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"snakes": []})

    def test_get_random_snakes_no_public_snakes(self):
        user = self.user_factory.login_as(self.client)
        self.snake_factory.basic(n=5, commit=True, account=user.account)
        self.assertEqual(Snake.objects.count(), 5)

        response = self.client.get("/account/games/create/json/random-snake/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"snakes": []})

    def test_get_random_snakes_self(self):
        user = self.user_factory.login_as(self.client)
        snakes = self.snake_factory.basic(n=5, commit=True, account=user.account)
        for snake in snakes:
            snake.is_public = True
            snake.save()
        snake_ids = [s.id for s in snakes]

        response = self.client.get("/account/games/create/json/random-snake/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("snakes", response.json())
        self.assertEqual(len(response.json()["snakes"]), 1)
        self.assertIn(response.json()["snakes"][0], snake_ids)

    def test_get_random_snakes_self_multi(self):
        user = self.user_factory.login_as(self.client)
        snakes = self.snake_factory.basic(n=5, commit=True, account=user.account)
        for snake in snakes:
            snake.is_public = True
            snake.save()
        snake_ids = [s.id for s in snakes]

        response = self.client.get("/account/games/create/json/random-snake/?count=3")

        self.assertEqual(response.status_code, 200)
        self.assertIn("snakes", response.json())
        self.assertEqual(len(response.json()["snakes"]), 3)
        self.assertEqual(len(set(response.json()["snakes"])), 3)
        self.assertIn(response.json()["snakes"][0], snake_ids)
        self.assertIn(response.json()["snakes"][1], snake_ids)
        self.assertIn(response.json()["snakes"][2], snake_ids)

    def test_get_random_snakes_other_user(self):
        other_user = self.user_factory.basic(email="other@test.com", commit=True)

        snake = self.snake_factory.basic(commit=True, account=other_user.account)
        snake.is_public = True
        snake.save()

        self.user_factory.login_as(self.client)
        response = self.client.get("/account/games/create/json/random-snake/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("snakes", response.json())
        self.assertEqual(len(response.json()["snakes"]), 1)
        self.assertEqual(response.json()["snakes"][0], snake.id)

    def test_get_snake_autocomplete_by_username(self):
        user = self.user_factory.login_as(self.client)

        snake1 = self.snake_factory.basic(account=user.account)
        snake1.name = "snaker one"
        snake1.save()

        response = self.client.get(
            f"/account/games/create/json/snake-autocomplete/?q={user.username}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(
            response.json()[0], {"value": snake1.id, "text": snake1.public_name}
        )

        snake2 = self.snake_factory.basic(account=user.account)
        snake2.name = "snaker two"
        snake2.save()

        response = self.client.get(
            f"/account/games/create/json/snake-autocomplete/?q={user.username}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertIn(snake1.id, [s["value"] for s in response.json()])
        self.assertIn(snake2.id, [s["value"] for s in response.json()])
        self.assertIn(snake1.public_name, [s["text"] for s in response.json()])
        self.assertIn(snake2.public_name, [s["text"] for s in response.json()])

    def test_get_snake_autocomplete_by_snake_name(self):
        user = self.user_factory.login_as(self.client)

        snake1 = self.snake_factory.basic(account=user.account)
        snake1.name = "snaker one"
        snake1.save()

        snake2 = self.snake_factory.basic(account=user.account)
        snake2.name = "snaker two"
        snake2.save()

        response = self.client.get(
            f"/account/games/create/json/snake-autocomplete/?q=one"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(
            response.json()[0], {"value": snake1.id, "text": snake1.public_name}
        )

        response = self.client.get(
            f"/account/games/create/json/snake-autocomplete/?q=snaker"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertIn(snake1.id, [s["value"] for s in response.json()])
        self.assertIn(snake2.id, [s["value"] for s in response.json()])
        self.assertIn(snake1.public_name, [s["text"] for s in response.json()])
        self.assertIn(snake2.public_name, [s["text"] for s in response.json()])

    def test_get_snake_info(self):
        user = self.user_factory.login_as(self.client)

        snake1 = self.snake_factory.basic(account=user.account)
        snake1.name = "snaker one"
        snake1.save()

        snake2 = self.snake_factory.basic(account=user.account)
        snake2.name = "snaker two"
        snake2.save()

        snake_ids = f"{snake1.id},{snake2.id}"
        response = self.client.get(
            f"/account/games/create/json/snake-info/?snakes={snake_ids}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertIn(snake1.id, [s["value"] for s in response.json()])
        self.assertIn(snake2.id, [s["value"] for s in response.json()])
        self.assertIn(snake1.public_name, [s["text"] for s in response.json()])
        self.assertIn(snake2.public_name, [s["text"] for s in response.json()])

    def test_get_snake_info_other_snakes(self):
        other_user = self.user_factory.basic(email="other@test.com", commit=True)

        snake1 = self.snake_factory.basic(account=other_user.account)
        snake1.name = "snaker one"
        snake1.save()

        snake2 = self.snake_factory.basic(account=other_user.account)
        snake2.name = "snaker two"
        snake2.save()

        snake_ids = f"{snake1.id},{snake2.id}"

        self.user_factory.login_as(self.client)
        response = self.client.get(
            f"/account/games/create/json/snake-info/?snakes={snake_ids}"
        )

        self.assertEqual(Snake.objects.count(), 2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_get_snake_info_other_snakes_public(self):
        other_user = self.user_factory.basic(email="other@test.com", commit=True)

        snake1 = self.snake_factory.basic(account=other_user.account)
        snake1.name = "snaker one"
        snake1.is_public = True
        snake1.save()

        snake2 = self.snake_factory.basic(account=other_user.account)
        snake2.name = "snaker two"
        snake2.is_public = True
        snake2.save()

        snake_ids = f"{snake1.id},{snake2.id}"

        self.user_factory.login_as(self.client)
        response = self.client.get(
            f"/account/games/create/json/snake-info/?snakes={snake_ids}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertIn(snake1.id, [s["value"] for s in response.json()])
        self.assertIn(snake2.id, [s["value"] for s in response.json()])
        self.assertIn(snake1.public_name, [s["text"] for s in response.json()])
        self.assertIn(snake2.public_name, [s["text"] for s in response.json()])


class CreateSnakeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_factory = UserFactory()

    def test_anonymous(self):
        response = self.client.get("/account/snakes/create/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/account/snakes/create/")

    def test_get(self):
        self.user_factory.login_as(self.client)
        response = self.client.get("/account/snakes/create/")

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        user = self.user_factory.login_as(self.client)
        response = self.client.post(
            "/account/snakes/create/",
            {"name": "My Snake", "url": "https://dedsnek.herokuapp.com"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(f"/profile/{user.account.profile_slug}", response.url)

        snakes = Snake.objects.filter(account=user.account)
        self.assertEqual(snakes.count(), 1)

        snake = snakes.first()
        self.assertEqual(snake.name, "My Snake")
        self.assertEqual(snake.url, "https://dedsnek.herokuapp.com")
        self.assertIsNotNone(snake.account)


class SettingsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_factory = UserFactory()

    def test_anonymous(self):
        response = self.client.get("/account/settings/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/account/settings/")

    def test_settings(self):
        self.user_factory.login_as(self.client)
        response = self.client.get("/account/settings/")
        self.assertEqual(response.status_code, 200)

    def test_settings_update(self):
        user = self.user_factory.login_as(self.client)
        response = self.client.post(
            "/account/settings/",
            {
                "email": "test@battlesnake.com",
                "display_name": "Test User Primo",
                "profile_slug": "NEW-PROFILE-SLUG",
                "country": "DE",
                "bio": "my new bio",
                "years_programming": "0-2",
            },
        )

        self.assertEqual(response.status_code, 302)
        account = Account.objects.get(user=user)
        self.assertEqual(account.user.email, "test@battlesnake.com")
        self.assertEqual(account.display_name, "Test User Primo")
        self.assertEqual(account.profile_slug, "new-profile-slug")
        self.assertEqual(account.country, "DE")
        self.assertEqual(account.bio, "my new bio")
        self.assertEqual(account.years_programming, "0-2")

    def test_settings_update_no_email(self):
        self.user_factory.login_as(self.client)
        response = self.client.post("/account/settings/", {"email": ""})

        self.assertEqual(response.status_code, 400)
