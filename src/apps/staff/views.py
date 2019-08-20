from collections import Counter
from datetime import datetime, timedelta

from django.shortcuts import render
from pytz import utc

from apps.authentication.decorators import admin_required
from apps.authentication.models import User
from apps.core.models import Game, Profile, Snake
import util.time


@admin_required
def index(request):
    num_users = User.objects.all().count()
    num_snakes = Snake.objects.all().count()
    num_games = Game.objects.all().count()

    return render(
        request,
        "staff/index.html",
        {"num_users": num_users, "num_snakes": num_snakes, "num_games": num_games},
    )


@admin_required
def histograms(request):
    def now():
        return datetime.utcnow().replace(tzinfo=utc)

    def floor_to_month(dt):
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    profile_createds = [
        dt.strftime("%Y-%m")
        for dt in Profile.objects.all()
        .order_by("created")
        .values_list("created", flat=True)
    ]
    profile_created_histogram = Counter()

    user_createds = [
        dt.strftime("%Y-%m")
        for dt in User.objects.all()
        .order_by("created")
        .values_list("created", flat=True)
    ]
    user_created_histogram = Counter()

    dt = util.time.from_unix_timestamp(1546300800)  # Jan 1 2019
    while dt < now():
        dt_str = dt.strftime("%Y-%m")
        profile_created_histogram[dt_str] = profile_createds.count(dt_str)
        user_created_histogram[dt_str] = user_createds.count(dt_str)

        dt = floor_to_month(dt + timedelta(days=32))

    return render(
        request,
        "staff/histograms.html",
        {
            "profile_created": list(profile_created_histogram.items()),
            "user_created": list(user_created_histogram.items()),
        },
    )
