from django.contrib import admin

from apps.common.models import BaseModelAdmin
from .models import Account, Game, Profile, Snake


@admin.register(Account)
class AccountAdmin(BaseModelAdmin):
    readonly_fields = BaseModelAdmin.readonly_fields + ("id", "user")


@admin.register(Game)
class GameAdmin(BaseModelAdmin):
    list_display = ["engine_id", "width", "height", "status", "turn"]
    search_fields = ["engine_id", "id"]


@admin.register(Profile)
class ProfileAdmin(BaseModelAdmin):
    search_fields = ["user__username"]
    autocomplete_fields = ["user"]


@admin.register(Snake)
class SnakeAdmin(BaseModelAdmin):
    search_fields = ["profile__user__username", "name"]
    ordering = ["profile__user__username", "name"]
    autocomplete_fields = ["profile"]
    list_display = ["public_name", "is_public"]
