from django.contrib import admin

from apps.common.models import BaseModelAdmin
from .models import Account, Game, Profile, Snake


@admin.register(Account)
class AccountAdmin(BaseModelAdmin):
    readonly_fields = BaseModelAdmin.readonly_fields + ("id", "user")
    search_fields = ("user__username", "id")


@admin.register(Game)
class GameAdmin(BaseModelAdmin):
    list_display = ("engine_id", "width", "height", "status", "turn")
    search_fields = ("engine_id", "id")


@admin.register(Profile)
class ProfileAdmin(BaseModelAdmin):
    search_fields = ("user__username",)
    autocomplete_fields = ("user",)


@admin.register(Snake)
class SnakeAdmin(BaseModelAdmin):
    search_fields = ("account__user__username", "name")
    ordering = ("account__user__username", "name")
    autocomplete_fields = ("account", "profile")
    list_display = ("public_name", "is_public")
