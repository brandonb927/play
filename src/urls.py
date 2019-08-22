from urllib.parse import urlencode

from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path, reverse

import apps.pages.views


# This needs to happen BEFORE we register any URLs
def redirect_to_login(request):
    params = ""
    if request.GET:
        params = f"?{urlencode(request.GET)}"
    return redirect(f"{reverse('login')}{params}")


def redirect_to_logout(request):
    params = ""
    if request.GET:
        params = f"?{urlencode(request.GET)}"
    return redirect(f"{reverse('logout')}{params}")


admin.site.login = redirect_to_login
admin.site.logout = redirect_to_logout


if settings.MAINTENANCE_MODE:
    urlpatterns = [path("admin/", admin.site.urls)]
    # In maintenance mode, everything is handled via 404 (which will respond 200)
    handler404 = apps.pages.views.handle404_maintenance

else:
    urlpatterns = [
        path("admin/", admin.site.urls),
        path("staff/", include("apps.staff.urls")),
        path("", include("apps.authentication.urls")),
        path("", include("apps.core.urls")),
        path("", include("apps.leaderboard.urls")),
        path("", include("apps.pages.urls")),
    ]
    handler403 = apps.pages.views.handle403
    handler404 = apps.pages.views.handle404
    handler500 = apps.pages.views.handle500
