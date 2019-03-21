from apps.core.models import Profile, Snake
from apps.authentication.factories import UserFactory

user_factory = UserFactory()


def test_get(client):
    user = user_factory.login_as(client)
    response = client.get(f"/u/{user.username}/")
    assert response.status_code == 200


def test_get_case_insensitive(client):
    user = user_factory.login_as(client)
    response = client.get(f"/u/{user.username.upper()}/")
    assert response.status_code == 302
    assert response.url == f"/u/{user.username}/"


def test_snakes_are_returned_in_response(client):
    user = user_factory.login_as(client)
    Snake.objects.create(profile=user.profile, name="My Snake")
    response = client.get(f"/u/{user.username}/")

    assert response.context[-1]["profile"].user.profile.snakes[0].name == "My Snake"


def test_edit(client):
    user_factory.login_as(client)
    response = client.get("/settings/")
    assert response.status_code == 200


def test_update(client):
    user = user_factory.login_as(client)
    response = client.post("/settings/", {"email": "my-new-email", "_method": "PUT"})
    assert response.status_code == 302
    assert Profile.objects.get(user=user).email == "my-new-email"


def test_update_no_email(client):
    user_factory.login_as(client)
    response = client.post("/settings/", {"email": "", "_method": "PUT"})
    assert response.status_code == 400


def test_delete(client):
    user_factory.login_as(client)
    response = client.delete("/settings/")
    assert response.status_code == 302


def test_delete_no_profile(client):
    user_factory.login_as(client)
    response = client.delete("/settings/")
    assert response.status_code == 302
