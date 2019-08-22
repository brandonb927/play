from social_core.exceptions import AuthForbidden

from apps.core.models import Account


def blacklist_usernames(backend, details, response, *args, **kwargs):
    # We reserve these usernames for our own purposes.
    if kwargs.get("username") in ["battlesnake", "battlesnakeio", "battle-snake"]:
        raise AuthForbidden(backend)


def create_account(backend, details, user, *args, **kwargs):
    Account.objects.create_for_user(user)
