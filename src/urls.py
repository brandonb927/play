from django.conf import settings
from django.contrib import admin
from django.urls import include, path

import apps.authentication.views
import apps.pages.views

admin.site.login = apps.authentication.views.send_to_login

if settings.MAINTENANCE_MODE:
    urlpatterns = [path("admin/", admin.site.urls)]
    handler404 = apps.pages.views.handle404_maintenance

else:
    urlpatterns = [
        path("admin/", admin.site.urls),
        path("staff/", include("apps.staff.urls")),
        path("", include("apps.authentication.urls")),
        path("", include("apps.core.urls")),
        path("", include("apps.leaderboard.urls")),
        path("", include("apps.pages.urls")),
        path("", include("apps.tournament.urls")),
    ]
    handler403 = apps.pages.views.handle403
    handler404 = apps.pages.views.handle404
    handler500 = apps.pages.views.handle500

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
