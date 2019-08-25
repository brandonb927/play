from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render


def force_403(request, exception=None):
    raise PermissionDenied("forbidden (forced)")


def force_404(request, exception=None):
    raise Http404("not found (forced)")


def force_500(request):
    class ForcedException(Exception):
        pass

    raise ForcedException("internal server error (forced)")


def handle_403(request, exception=None):
    return render(request, "ui/pages/403.html", status=403)


def handle_404(request, exception=None):
    return render(request, "ui/pages/404.html", status=404)


def handle_500(request):
    return render(request, "ui/pages/500.html", status=500)


def handle_maintenance(request, exception=None):
    return render(request, "ui/pages/maintenance.html", status=200)
