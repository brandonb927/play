from django.conf import settings
from django.db import models

from apps.common.fields import ShortUUIDField
from apps.common.models import BaseModel


class Account(BaseModel):
    id = ShortUUIDField(prefix="act", max_length=128, primary_key=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    marketing_optin = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f"Account[{self.id}]"
