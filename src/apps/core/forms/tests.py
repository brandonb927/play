from django.test import TestCase

from apps.authentication.factories import UserFactory
from apps.core.forms import GameForm, SnakeForm
from apps.core.factories import SnakeFactory
from apps.core.models import Game, Snake


class GameFormTestCase(TestCase):
    def setUp(self):
        self.snake_factory = SnakeFactory()
        self.user_factory = UserFactory()

    def test_game_form_save(self):
        user = self.user_factory.basic(commit=True)
        snake = self.snake_factory.basic(n=1, commit=True, profile=user.profile)

        form = GameForm(
            {"width": 10, "height": 10, "board_size": "custom", "snakes": snake.id}
        )

        self.assertTrue(form.is_valid())
        self.assertIsInstance(form.save(user), Game)

    def test_game_form_hidden_snake(self):
        user = self.user_factory.basic(commit=True)
        snake = self.snake_factory.basic(n=1, commit=True, profile=user.profile)

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
            user.profile,
            {"name": "DSnek", "url": "https://dsnek.herokuapp.com", "is_public": True},
        )
        form.save()
        user.refresh_from_db()
        snake = user.profile.snakes.get(name="DSnek")

        self.assertEqual(snake.url, "https://dsnek.herokuapp.com")
        self.assertTrue(snake.is_public)

    def test_update_existing_snake(self):
        user = self.user_factory.basic(commit=True)
        snake = Snake.objects.create(profile=user.profile, name="DSnek")

        self.assertEqual(snake.url, "")
        self.assertFalse(snake.is_public)

        form = SnakeForm(
            user.profile,
            {"name": "DSnek", "url": "https://dsnek.herokuapp.com", "is_public": True},
            instance=snake,
        )

        form.save()
        user.refresh_from_db()
        snake = user.profile.snakes.get(name="DSnek")

        self.assertEqual(snake.url, "https://dsnek.herokuapp.com")
        self.assertTrue(snake.is_public)

    def test_new_snake_with_name_collision(self):
        user = self.user_factory.basic(commit=True)
        Snake.objects.create(profile=user.profile, name="DSnek")
        form = SnakeForm(
            user.profile,
            {"name": "DSnek", "url": "https://dsnek.herokuapp.com", "is_public": True},
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_update_snake_with_name_collision(self):
        user = self.user_factory.basic(commit=True)
        Snake.objects.create(profile=user.profile, name="DSnek")
        snake = Snake.objects.create(profile=user.profile, name="DSnek1")

        form = SnakeForm(
            user.profile,
            {"name": "DSnek", "url": "https://dsnek.herokuapp.com", "is_public": True},
            instance=snake,
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
