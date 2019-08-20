import logging
import random

from django.shortcuts import render

from apps.core.models import Game


logger = logging.getLogger(__name__)


def index(request):
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
