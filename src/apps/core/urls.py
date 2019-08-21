from django.urls import path

from . import views

# from core.views import account, game, home, snake
from apps.common.routing import method_dispatch as route


urlpatterns = [
    path(
        "settings/",
        route(GET=views.account_edit, PUT=views.account_update),
        name="settings",
    ),
    path(
        "u/by-games-snake/<game_snake_id>/", route(GET=views.account_show_by_game_snake)
    ),
    path("u/<username>/", route(GET=views.account_show), name="u"),
    path("", route(GET=views.index), name="home"),
    path(
        "s/new/", route(GET=views.snake_new, POST=views.snake_create), name="new_snake"
    ),
    path(
        "s/<snake_id>/",
        route(GET=views.snake_show, DELETE=views.snake_delete),
        name="snake",
    ),
    path(
        "s/<snake_id>/edit/",
        route(GET=views.snake_edit, PUT=views.snake_update),
        name="snake_edit",
    ),
    path("g/new/", route(GET=views.game_new, POST=views.game_create), name="new_game"),
    path("g/snake-autocomplete/", route(GET=views.game_snake_autocomplete)),
    path("g/snake-info/", route(GET=views.game_snake_info)),
    path("g/random-public-snake/", route(GET=views.game_random_public_snake)),
    path("g/<engine_id>/", route(GET=views.game_show), name="game"),
    path("g/<engine_id>/gif/", route(GET=views.game_show_gif), name="game_gif"),
]
