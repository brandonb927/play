from django.urls import path

from apps.staff import views


app_name = "staff"
urlpatterns = [
    path("", views.index, name="index"),
    path("dump/teams/", views.dump_teams, name="dump-teams"),
    path("dump/teams-csv/", views.dump_teams_csvfile, name="dump-teams-csv"),
    path("dump/users/", views.dump_users, name="dump-users"),
    path("dump/users-csv/", views.dump_users_csvfile, name="dump-users-csv"),
    path("histograms/", views.histograms, name="histograms"),
    path(
        "tools/create-tournament-game/",
        views.tool_create_tournament_game,
        name="tool-create-tournament-game",
    ),
]
