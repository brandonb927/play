from django.conf import settings
from django.utils.http import urlquote

from apps.core.models import Game


def generate_game_url(game: Game):
    engine_url = settings.ENGINE_URL
    if game.engine_url is not None and len(game.engine_url) > 0:
        engine_url = game.engine_url

    return f"{settings.BOARD_URL}/?engine={urlquote(engine_url)}&game={game.engine_id}"


def generate_game_query_string(request):
    query_string_data = {}

    if request.GET.get("enableLinks"):
        query_string_data["enableLinks"] = "true"

    if request.GET.get("autoplay"):
        query_string_data["autoplay"] = "true"

    turn = request.GET.get("turn")
    if turn:
        query_string_data["turn"] = turn

    frame_rate = request.GET.get("frameRate")
    if frame_rate:
        query_string_data["frameRate"] = frame_rate

    board_theme = request.GET.get("boardTheme")
    if board_theme:
        query_string_data["boardTheme"] = board_theme

    # Profile might not exist here
    try:
        board_setting_overrides = request.profile.board_settings

        if board_setting_overrides["frame_rate"]:
            query_string_data["frameRate"] = board_setting_overrides["frame_rate"]

        if board_setting_overrides["theme"]:
            query_string_data["boardTheme"] = board_setting_overrides["theme"]
    except AttributeError:
        pass

    return query_string_data


def generate_exporter_url(engine_id):
    return f"{settings.EXPORTER_URL}/games/{engine_id}/gif"
