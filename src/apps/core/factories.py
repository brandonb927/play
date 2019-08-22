from apps.authentication.models import User
from apps.core.models import Account, Game, Snake


class GameFactory:
    def basic(self, commit=False, n=None, **kwargs):
        if n:
            return [self.basic(commit=commit, **kwargs) for _ in range(n)]
        game = Game(width=20, height=20, max_turns_to_next_food_spawn=12, **kwargs)
        if commit:
            game.save()
        return game


class SnakeFactory:
    def basic(self, n=1, commit=False, account: Account = None):
        if account is None:
            raise Exception("snake.account is required")
        if n > 1:
            return [self.basic(commit=commit, account=account) for _ in range(n)]
        snake = Snake(
            name="test", url="http://foo.bar.battkesnake.com", account=account
        )
        if commit:
            snake.save()
        return snake


class UserFactory:
    def basic(self, email="test@test.com", commit=False):
        username = email.split("@")[0]
        user = User(username=username, email=email)
        if commit:
            user.account = Account.objects.create(user=user)
            user.save()
        return user

    def login_as(self, client, email="test@test.com", is_superuser=False):
        user = self.basic(email=email, commit=True)
        user.is_superuser = is_superuser
        user.save()
        client.force_login(user)
        return user
