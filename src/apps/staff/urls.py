from django.urls import path

from apps.staff import views


app_name = "staff"
urlpatterns = [
    path("", views.index, name="index"),
    path("histograms/", views.histograms, name="histograms"),
    path("dump/teams/", views.dump_teams, name="dump-teams"),
    path("dump/users/", views.dump_users, name="dump-users"),
]
