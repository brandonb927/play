from django.conf import settings
from django.db import transaction
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.utils.http import urlencode

from apps.core.forms import GameForm
from apps.core.middleware import profile_required
from apps.core.models import Snake, Game
from apps.utils.helpers import (
    generate_game_url,
    generate_game_query_string,
    generate_exporter_url,
)


@profile_required
def new(request):
    snake_ids = request.GET.get("snake-ids")
    form = GameForm(initial={"snakes": snake_ids, "engine_url": settings.ENGINE_URL})
    return render(request, "core/game/new.html", {"form": form})


@profile_required
@transaction.atomic
def create(request):
    form = GameForm(request.POST)
    if form.is_valid():
        game = form.save(request.user)
        game.create()
        game.gamesnake_set.add()
        game.run()
        return redirect(f"/g/{game.engine_id}")
    return render(request, "core/game/new.html", {"form": form}, status=400)


@profile_required
def snake_autocomplete(request):
    q = request.GET.get("q")
    snakes = (
        Snake.objects.can_view(request.user)
        .by_public_name(q)
        .prefetch_related("profile__user")
    )
    return JsonResponse(
        [{"value": snake.id, "text": snake.public_name} for snake in snakes], safe=False
    )


@profile_required
def snake_info(request):
    snake_ids = request.GET.get("snakes", "").split(",")
    snakes = Snake.objects.can_view(request.user).filter(id__in=snake_ids)
    return JsonResponse(
        [{"value": snake.id, "text": snake.public_name} for snake in snakes], safe=False
    )


@profile_required
def random_public_snake(request):
    count = int(request.GET.get("count", 1))
    snakes = Snake.objects.filter(is_public=True).order_by("?")[:count]
    return JsonResponse({"snakes": [snake.id for snake in snakes]})


@profile_required
def show(request, engine_id):
    try:
        game = Game.objects.get(engine_id=engine_id)
    except Game.DoesNotExist:
        raise Http404

    profile = request.user.profile
    game_board_url = generate_game_url(game)
    query_string_data = generate_game_query_string(request)
    game_query_string = urlencode(query_string_data)
    game_board_url = f"{game_board_url}&{game_query_string}"

    return render(
        request,
        "core/game/show.html",
        {
            "url": game_board_url,
            "game_image": f"https://exporter.battlesnake.io/games/{game.engine_id}/gif",
            "game": game,
        },
    )


def show_gif(request, engine_id):
    try:
        game = Game.objects.get(engine_id=engine_id)
    except Game.DoesNotExist:
        raise Http404

    return redirect(generate_exporter_url(game.engine_id))
