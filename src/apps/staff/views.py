from collections import Counter
from datetime import datetime, timedelta

from django.shortcuts import render
from pytz import utc

from apps.authentication.decorators import admin_required
from apps.authentication.models import User
from apps.core.models import Account, Game, Snake
from apps.events.models import Team
from apps.staff.forms import CreateTournamentGameForm
import util.time


@admin_required
def index(request):
    num_accounts = Account.objects.all().count()
    num_snakes = Snake.objects.all().count()
    num_games = Game.objects.all().count()

    return render(
        request,
        "staff/index.html",
        {
            "num_accounts": num_accounts,
            "num_snakes": num_snakes,
            "num_games": num_games,
        },
    )


@admin_required
def dump_teams(request):
    title = "Dump Teams"
    rows = [("name", "division", "snake_name", "snake_url", "bio")] + list(
        Team.objects.all()
        .order_by("division", "name")
        .values_list("name", "division", "snake__name", "snake__url", "bio")
    )
    return render(request, "staff/dump.html", {"title": title, "rows": rows})


@admin_required
def dump_users(request):
    title = "Dump Users"
    rows = [("username", "email", "created")] + list(
        User.objects.all()
        .order_by("username")
        .values_list("username", "email", "created")
    )
    return render(request, "staff/dump.html", {"title": title, "rows": rows})


@admin_required
def histograms(request):
    def now():
        return datetime.utcnow().replace(tzinfo=utc)

    def floor_to_month(dt):
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    account_createds = [
        dt.strftime("%Y-%m")
        for dt in Account.objects.all()
        .order_by("created")
        .values_list("created", flat=True)
    ]
    account_created_histogram = Counter()

    dt = util.time.from_unix_timestamp(1546300800)  # Jan 1 2019
    while dt < now():
        dt_str = dt.strftime("%Y-%m")
        account_created_histogram[dt_str] = account_createds.count(dt_str)

        dt = floor_to_month(dt + timedelta(days=32))

    return render(
        request,
        "staff/histograms.html",
        {"account_created": list(account_created_histogram.items())},
    )


@admin_required
def tool_create_tournament_game(request):
    if request.method == "POST":
        form = CreateTournamentGameForm(request.POST)
        if form.is_valid():
            game = form.save()
    else:
        form = CreateTournamentGameForm()
        game = None
    return render(
        request, "staff/tool_create_tournament_game.html", {"form": form, "game": game}
    )
