from collections import Counter
from datetime import datetime, timedelta

from django.shortcuts import render
from pytz import utc

from apps.core.models import Profile
from apps.utils.decorators import superuser_required


@superuser_required
def index(request):
    return render(request, "staff/index.html")


@superuser_required
def user_report(request):
    def now():
        return datetime.utcnow().replace(tzinfo=utc)

    def floor_to_month(dt):
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    createds = (
        Profile.objects.all().order_by("created").values_list("created", flat=True)
    )
    results = Counter()

    dt = createds[0]
    while dt < now():
        dt_str = dt.strftime("%Y-%m")
        for created in createds:
            if created.strftime("%Y-%m") == dt_str:
                results[dt_str] += 1
        dt = floor_to_month(dt + timedelta(days=32))

    return render(request, "staff/user_report.html", {"data": list(results.items())})
