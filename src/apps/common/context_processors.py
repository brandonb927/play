from django.conf import settings


def common(request):
    return {
        "APP_VERSION": settings.APP_VERSION,
        "BOARD_URL": settings.BATTLESNAKE_ENGINE_URL,
        "ENGINE_URL": settings.BATTLESNAKE_ENGINE_URL,
    }
