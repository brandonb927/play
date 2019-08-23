from django.urls import path

from . import views

# from core.views import account, game, home, snake
from apps.common.routing import method_dispatch as route  # TODO: REMOVE ME


urlpatterns = [
    path("", views.HomepageView.as_view(), name="home"),
    path("u/<username>/", views.AccountView.as_view(), name="u"),
    path("settings/", views.AccountSettingsView.as_view(), name="settings"),
    path(
        "u/by-games-snake/<game_snake_id>/", route(GET=views.account_show_by_game_snake)
    ),
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
    path("g/<engine_id>/", views.GameView.as_view(), name="game"),
    path("g/<engine_id>/gif/", views.GameGIFView.as_view(), name="game_gif"),
]
