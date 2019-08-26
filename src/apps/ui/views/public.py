import logging
import random

from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

from apps.core.models import Account, Game, Snake


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
            "ui/pages/home.html",
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
            request, "ui/pages/account.html", {"account": account, "games": games}
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
            "ui/pages/game.html",
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


class SnakeView(View):
    def get(self, request, snake_id):
        snake = get_object_or_404(Snake, id=snake_id)
        games = (
            snake.games.watchable()
            .order_by("-created")
            .prefetch_related("gamesnake_set__snake")[:10]
        )
        return render(request, "ui/pages/snake.html", {"snake": snake, "games": games})