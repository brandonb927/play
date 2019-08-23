from django.urls import path

from apps.ui.views import account
from apps.ui.views import public


urlpatterns = [
    # Public URLs
    path("", public.HomepageView.as_view(), name="home"),
    path("g/<engine_id>/", public.GameView.as_view(), name="game"),
    path("g/<engine_id>/gif/", public.GameGIFView.as_view(), name="game_gif"),
    path("s/<snake_id>/", public.SnakeView.as_view(), name="snake"),
    path("u/<username>/", public.AccountView.as_view(), name="u"),
    # Account Specific URLs
    path("account/settings/", account.SettingsView.as_view(), name="settings"),
    path("account/games/create/", account.CreateGameView.as_view(), name="new_game"),
    path(
        "account/games/create/json/<func>/", account.CreateGameJSONHelpersView.as_view()
    ),
    path("account/snakes/create/", account.CreateSnakeView.as_view(), name="new_snake"),
]
