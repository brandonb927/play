from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager as DjangoUserManager,
)

from apps.common.fields import ShortUUIDField
from apps.common.models import BaseModel


class UserManager(DjangoUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        return super()._create_user(username, email, password)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    id = ShortUUIDField(prefix="usr", max_length=128, primary_key=True)

    username = models.CharField(
        max_length=39, unique=True
    )  # 39 is max GitHub username length
    email = models.CharField(max_length=512)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_commentator = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return f"User[{self.username}]"
