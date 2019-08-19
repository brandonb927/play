from django.contrib import admin

from util.models import BaseModelAdmin
from .models import Game, Profile, Snake


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
