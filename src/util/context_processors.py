from django.conf import settings


def window_globals(request):
    return {
        "ENGINE_URL": settings.BATTLESNAKE_ENGINE_URL,
        "BOARD_URL": settings.BATTLESNAKE_ENGINE_URL,
    }
