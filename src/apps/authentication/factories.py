from apps.authentication.models import User
from apps.core.models import Account, Profile


class UserFactory:
    def basic(self, email="test@test.com", commit=False):
        username = email.split("@")[0]
        user = User(username=username, email=email)
        if commit:
            user.profile = Profile.objects.create(user=user)
            user.account = Account.objects.create(user=user)
            user.save()
        return user

    def login_as(self, client, email="test@test.com", is_superuser=False):
        user = self.basic(email=email, commit=True)
        user.is_superuser = is_superuser
        user.save()
        client.force_login(user)
        return user
