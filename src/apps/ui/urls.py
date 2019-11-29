from urllib.parse import urlencode

from django.shortcuts import redirect
from django.urls import path
from django.views.generic import TemplateView

from apps.ui.views import account
from apps.ui.views import error
from apps.ui.views import public


class EXTERNAL_URLS:
    BLOG = "https://medium.com/battlesnake"
    DOCS = "https://docs.battlesnake.com"
    FACEBOOK = "https://www.facebook.com/Battlesnake-109244433855215/"
    FAQ = "https://docs.battlesnake.com/faq"
    GITHUB = "https://github.com/battlesnakeio"
    HIGHLIGHTS = "https://www.youtube.com/watch?v=d9ARbSzBKxc"
    INSTAGRAM = "https://www.instagram.com/battlesnakeofficial/"
    SLACK = "https://join.slack.com/t/battlesnake/shared_invite/enQtNzM4NDQ3MjgyMjI0LWJkZGJkOTg3NTAyNjg2MWVhMzk5OTVlMjk2ZjIzMWUxMWQ3MzYxN2I4YTY4YTE0YTI0MmQ4MzdiODNiZTgyZGE"
    STORE = "https://shop.spreadshirt.com/battlesnake"
    TWITTER = "https://twitter.com/battlesnakeio"
    TWITCH = "https://twitch.tv/BattlesnakeOfficial"
    YOUTUBE = "https://www.youtube.com/channel/UClaK3LSm3OfsOgfyjWG6SMw"
    ZOOM = "https://zoom.us/j/8867080744"


def external(path):
    def redirector(request):
        query_string = urlencode(request.GET)
        url = f"{path}"
        if query_string:
            url = f"{url}?{query_string}"
        return redirect(url)

    return redirector


def template(template_name, exception=None):
    return TemplateView.as_view(template_name=template_name)


urlpatterns = [
    # Public Content URLs
    path("", public.HomepageView.as_view(), name="home"),
    path("careers/", public.JobsView.as_view(), name="jobs"),
    path("careers/<job_post_id>/", public.JobsView.as_view(), name="job_post"),
    path("events/", public.EventsView.as_view(), name="events"),
    path("events/<slug:event_slug>/", public.EventsView.as_view(), name="event"),
    path("g/<engine_id>/", public.GameView.as_view(), name="game"),
    path("g/<engine_id>/gif/", public.GameGIFView.as_view(), name="game_gif"),
    path("s/<snake_id>/", public.SnakeView.as_view(), name="snake"),
    # TODO - remove this one to replace with profile slug URL
    path("u/<username>/", public.AccountView.as_view(), name="u"),
    path("profile/<slug:username>/", public.ProfileView.as_view(), name="profile"),
    # Account Specific URLs
    path("account/settings/", account.SettingsView.as_view(), name="settings"),
    path("account/games/create/", account.CreateGameView.as_view(), name="new_game"),
    path(
        "account/games/create/json/<func>/", account.CreateGameJSONHelpersView.as_view()
    ),
    path("account/report/", account.CreateContentReportView.as_view()),
    path("account/snakes/create/", account.CreateSnakeView.as_view(), name="new_snake"),
    path(
        "account/snakes/<snake_id>/", account.EditSnakeView.as_view(), name="edit-snake"
    ),
    path(
        "account/snakes/<snake_id>/delete/",
        account.DeleteSnakeView.as_view(),
        name="delete-snake",
    ),
    path(
        "events/<slug:event_slug>/register/",
        account.EventRegistrationView.as_view(),
        name="event-registration",
    ),
    # Static Content URLs
    path("about/contact/", template("ui/pages/contact.html"), name="contact"),
    path("about/conduct/", template("ui/pages/conduct.html"), name="conduct"),
    path("about/diversity/", template("ui/pages/diversity.html"), name="diversity"),
    path("about/mission/", template("ui/pages/mission.html"), name="mission"),
    path("privacy/", template("ui/pages/privacy.html"), name="privacy"),
    path("terms/", template("ui/pages/terms.html"), name="terms"),
    # Tracked Landing URLs
    path("reinvent/", template("ui/pages/reinvent.html"), name="landing-reinvent"),
    # Exernal Redirect URLs
    path("blog/", external(EXTERNAL_URLS.BLOG), name="external-blog"),
    path("docs/", external(EXTERNAL_URLS.DOCS), name="external-docs"),
    path("faq/", external(EXTERNAL_URLS.FAQ), name="external-faq"),
    path("facebook/", external(EXTERNAL_URLS.FACEBOOK), name="external-facebook"),
    path("github/", external(EXTERNAL_URLS.GITHUB), name="external-github"),
    path("instagram/", external(EXTERNAL_URLS.INSTAGRAM), name="external-instagram"),
    path("highlights/", external(EXTERNAL_URLS.HIGHLIGHTS), name="external-highlights"),
    path("slack/", external(EXTERNAL_URLS.SLACK), name="external-slack"),
    path("store/", external(EXTERNAL_URLS.STORE), name="external-store"),
    path("twitch/", external(EXTERNAL_URLS.TWITCH), name="external-twitch"),
    path("twitter/", external(EXTERNAL_URLS.TWITTER), name="external-twitter"),
    path("youtube/", external(EXTERNAL_URLS.YOUTUBE), name="external-youtube"),
    path("zoom/", external(EXTERNAL_URLS.ZOOM), name="external-zoom"),
    # Helpful Debug Pages
    path("debug/403/", error.force_403),
    path("debug/404/", error.force_404),
    path("debug/500/", error.force_500),
]
