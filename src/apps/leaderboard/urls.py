from django.http import HttpResponseNotAllowed
from django.urls import path

from apps.leaderboard import views


def route(**table):
    def invalid_method(request, *args, **kwargs):
        return HttpResponseNotAllowed(table.keys())

    def route(request, *args, **kwargs):
        method = request.method
        if request.POST and "_method" in request.POST:
            method = request.POST["_method"]
        method = method.upper()
        handler = table.get(method, invalid_method)
        return handler(request, *args, **kwargs)

    return route


urlpatterns = [
    path("leaderboard/", route(GET=views.leaderboard.index), name="leaderboard"),
    path(
        "leaderboard/snakes/", route(GET=views.snakes.index), name="leaderboard_snakes"
    ),
    path(
        "leaderboard/snakes/<snake_id>/",
        route(POST=views.snakes.create, DELETE=views.snakes.delete),
        name="leaderboard_snakes_action",
    ),
]
