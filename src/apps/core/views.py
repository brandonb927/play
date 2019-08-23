import logging
import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

from apps.core.forms import AccountForm, GameForm, SnakeForm
from apps.core.models import Account, Game, GameSnake, Snake


logger = logging.getLogger(__name__)


class HomepageView(View):
    def get(self, request):
        games = list(
            Game.objects.filter(status=Game.Status.COMPLETE, turn__gte=100)
            .prefetch_related("gamesnake_set")
            .order_by("-created")[:40]
        )
        random.shuffle(games)
        games = [g for g in games if g.gamesnake_set.count() > 1]
        return render(
            request,
            "core/home.html",
            {
                "games": [
                    {
                        "url": g.get_board_url()
                        + "&autoplay=true&hideScoreboard=true&hideMediaControls=true&frameRate=6",
                        "engine_id": g.engine_id,
                    }
                    for g in games[:4]
                ]
            },
        )


class AccountSettingsView(LoginRequiredMixin, View):
    def get(self, request):
        account = get_object_or_404(Account, user=request.user)
        form = AccountForm(instance=account)

        return render(
            request, "core/account/edit.html", {"form": form, "account": account}
        )

    def post(self, request):
        account = get_object_or_404(Account, user=request.user)
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Account updated!")
            return redirect("u", account.user.username)
        return render(
            request,
            "core/account/edit.html",
            {"form": form, "account": account},
            status=400,
        )


class AccountView(View):
    def get(self, request, username):
        # Case-insensitive lookup, redirects to correct URL
        account = get_object_or_404(Account, user__username__iexact=username)
        if account.user.username != username:
            return redirect("u", account.user.username)

        games = (
            Game.objects.filter(snakes__account=account)
            .watchable()
            .order_by("-created")
            .prefetch_related("gamesnake_set__snake")
            .distinct()[:10]
        )

        return render(
            request, "core/account/show.html", {"account": account, "games": games}
        )


class GameView(View):
    def get(self, request, engine_id):
        game = get_object_or_404(Game, engine_id=engine_id)
        game_board_url = game.get_board_url()

        if request.GET.get("enableLinks"):
            game_board_url = f"{game_board_url}&enableLinks=true"

        autoplay = request.GET.get("autoplay")
        if autoplay:
            game_board_url = f"{game_board_url}&autoplay=true"

        turn = request.GET.get("turn")
        if turn:
            game_board_url = f"{game_board_url}&turn={turn}"

        frame_rate = request.GET.get("frameRate")
        if frame_rate:
            game_board_url = f"{game_board_url}&frameRate={frame_rate}"

        return render(
            request,
            "core/game/show.html",
            {
                "url": game_board_url,
                "game_image": f"https://exporter.battlesnake.com/games/{game.engine_id}/gif",
                "game": game,
            },
        )


class GameGIFView(View):
    def get(self, request, engine_id):
        game = get_object_or_404(Game, engine_id=engine_id)
        return redirect(game.get_gif_url())


@login_required
def account_show_by_game_snake(request, game_snake_id):
    try:
        game_snake = GameSnake.objects.get(id=game_snake_id)
    except GameSnake.DoesNotExist:
        raise Http404
    return redirect("u", game_snake.snake.account.user.username)


@login_required
def game_new(request):
    snake_ids = request.GET.get("snake-ids")
    form = GameForm(
        initial={"snakes": snake_ids, "engine_url": settings.BATTLESNAKE_ENGINE_URL}
    )
    return render(request, "core/game/new.html", {"form": form})


@login_required
@transaction.atomic
def game_create(request):
    form = GameForm(request.POST)
    if form.is_valid():
        game = form.save(request.user)
        game.create()
        game.gamesnake_set.add()
        game.run()
        return redirect(f"/g/{game.engine_id}")
    return render(request, "core/game/new.html", {"form": form}, status=400)


@login_required
def game_snake_autocomplete(request):
    q = request.GET.get("q")
    snakes = (
        Snake.objects.can_view(request.user)
        .by_public_name(q)
        .prefetch_related("account__user")
    )
    return JsonResponse(
        [{"value": snake.id, "text": snake.public_name} for snake in snakes], safe=False
    )


@login_required
def game_snake_info(request):
    snake_ids = request.GET.get("snakes", "").split(",")
    snakes = Snake.objects.can_view(request.user).filter(id__in=snake_ids)
    return JsonResponse(
        [{"value": snake.id, "text": snake.public_name} for snake in snakes], safe=False
    )


@login_required
def game_random_public_snake(request):
    count = int(request.GET.get("count", 1))
    snakes = Snake.objects.filter(is_public=True).order_by("?")[:count]
    return JsonResponse({"snakes": [snake.id for snake in snakes]})


def snake_show(request, snake_id):
    snake = Snake.objects.get(id=snake_id)
    games = (
        snake.games.watchable()
        .order_by("-created")
        .prefetch_related("gamesnake_set__snake")[:10]
    )
    return render(request, "core/snake/show.html", {"snake": snake, "games": games})


@login_required
def snake_new(request):
    form = SnakeForm(request.user.account)
    return render(request, "core/snake/new.html", {"form": form})


@login_required
def snake_create(request):
    form = SnakeForm(request.user.account, request.POST)
    if form.is_valid():
        snake = form.save()
        messages.add_message(
            request, messages.SUCCESS, f"{snake.name} created successfully"
        )
        return redirect(f"/u/{request.user.username}")
    return render(request, "core/snake/edit.html", {"form": form})


@login_required
def snake_edit(request, snake_id):
    try:
        snake = request.user.account.snakes.get(id=snake_id)
        form = SnakeForm(request.user.account, instance=snake)
        return render(request, "core/snake/edit.html", {"form": form})
    except Snake.DoesNotExist:
        return redirect(f"/s/{snake_id}")


@login_required
def snake_update(request, snake_id):
    snake = request.user.account.snakes.get(id=snake_id)
    form = SnakeForm(request.user.account, request.POST, instance=snake)
    if form.is_valid():
        snake = form.save()
        messages.add_message(
            request, messages.SUCCESS, f"{snake.name} updated successfully"
        )
        return redirect(f"/u/{request.user.username}")
    return render(request, "core/snake/edit.html", {"form": form})


@login_required
def snake_delete(request, snake_id):
    snake = request.user.account.snakes.get(id=snake_id)
    snake.delete()
    messages.add_message(
        request, messages.SUCCESS, f"{snake.name} deleted successfully"
    )
    return redirect(f"/u/{request.user.username}")
