from django.contrib import admin
from django.contrib.auth.models import Group

from social_django.models import Association, Nonce, UserSocialAuth

from apps.authentication.models import User
from apps.common.models import BaseModelAdmin


@admin.register(User)
class UserAdmin(BaseModelAdmin):
    readonly_fields = BaseModelAdmin.readonly_fields + ("id",)
    exclude = ("password", "groups", "user_permissions")
    search_fields = ["username"]
    ordering = ["username"]


admin.site.unregister(Association)
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)
admin.site.unregister(Group)
