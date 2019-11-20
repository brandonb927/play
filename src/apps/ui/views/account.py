import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

import services.slack

from apps.core.models import Account, ContentReport, Snake
from apps.events.models import Event, Team
from apps.ui.forms import AccountForm, GameForm, EventRegistrationForm, SnakeForm


logger = logging.getLogger(__name__)


class CreateGameView(LoginRequiredMixin, View):
    def get(self, request):
        snake_ids = request.GET.get("snake-ids")
        form = GameForm(
            initial={"snakes": snake_ids, "engine_url": settings.BATTLESNAKE_ENGINE_URL}
        )
        return render(request, "ui/pages/create_game.html", {"form": form})

    def post(self, request):
        form = GameForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                game = form.save(request.user)
                game.create()
                game.gamesnake_set.add()
                game.run()
            return redirect(f"/g/{game.engine_id}")
        return render(request, "ui/pages/create_game.html", {"form": form}, status=400)


class CreateGameJSONHelpersView(View):
    def get(self, request, func):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        if func == "snake-autocomplete":
            return self._get_snake_autocomplete(request)
        if func == "snake-info":
            return self._get_snake_info(request)
        if func == "random-snake":
            return self._get_random_snake(request)

        raise Http404()

    def _get_snake_autocomplete(self, request):
        q = request.GET.get("q")
        snakes = (
            Snake.objects.can_view(request.user)
            .by_public_name(q)
            .prefetch_related("account__user")
        )
        return JsonResponse(
            [{"value": snake.id, "text": snake.public_name} for snake in snakes],
            safe=False,
        )

    def _get_snake_info(self, request):
        snake_ids = request.GET.get("snakes", "").split(",")
        snakes = Snake.objects.can_view(request.user).filter(id__in=snake_ids)
        return JsonResponse(
            [{"value": snake.id, "text": snake.public_name} for snake in snakes],
            safe=False,
        )

    def _get_random_snake(self, request):
        count = int(request.GET.get("count", 1))
        snakes = Snake.objects.filter(is_public=True).order_by("?")[:count]
        return JsonResponse({"snakes": [snake.id for snake in snakes]})


class CreateContentReportView(LoginRequiredMixin, View):
    # Accepts POST request from ANY URL
    def post(self, request):
        url = request.POST.get("report_url", "")
        text = request.POST.get("report_content", "")

        report = ContentReport.objects.create(
            account=request.user.account, url=url, text=text
        )

        messages.add_message(
            request,
            messages.INFO,
            "Your report has been logged. Our team will review shortly.",
        )
        services.slack.SlackClient().send_message(
            f":exclamation: Content Reported: id={report.id}"
        )

        return redirect(url)


class CreateSnakeView(LoginRequiredMixin, View):
    def get(self, request):
        form = SnakeForm(request.user.account)
        return render(
            request,
            "ui/pages/create_snake.html",
            {"form_title": "Create New Snake", "form": form},
        )

    def post(self, request):
        form = SnakeForm(request.user.account, request.POST)
        if form.is_valid():
            snake = form.save()
            messages.add_message(
                request, messages.SUCCESS, f"{snake.name} created successfully"
            )
            return redirect(f"/u/{request.user.username}")
        return render(
            request,
            "ui/pages/create_snake.html",
            {"form_title": "Create New Snake", "form": form},
        )


class EditSnakeView(LoginRequiredMixin, View):
    def get(self, request, snake_id):
        snake = get_object_or_404(Snake, id=snake_id, account=request.user.account)
        form = SnakeForm(request.user.account, instance=snake)
        return render(
            request,
            "ui/pages/create_snake.html",
            {"form_title": "Edit Snake", "form": form},
        )

    def post(self, request, snake_id):
        snake = get_object_or_404(Snake, id=snake_id, account=request.user.account)
        form = SnakeForm(request.user.account, instance=snake, data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, f"Updated {snake.name}.")
            return redirect(f"/u/{request.user.username}")
        return render(
            request,
            "ui/pages/create_snake.html",
            {"form_title": "Edit Snake", "form": form},
        )


class DeleteSnakeView(LoginRequiredMixin, View):
    def post(self, request, snake_id):
        snake = get_object_or_404(Snake, id=snake_id, account=request.user.account)
        snake.delete()
        messages.add_message(request, messages.INFO, f"Deleted {snake.name}.")
        return redirect(f"/u/{request.user.username}")


class EventRegistrationView(View):
    def get(self, request, event_slug):
        event = get_object_or_404(
            Event.objects.get_listed_events(), slug=event_slug, allow_registration=True
        )
        if not request.user.is_authenticated:
            return render(request, "ui/pages/event_registration.html", {"event": event})

        if event.is_account_registered(request.user.account):
            team = Team.objects.get(event=event, accounts=request.user.account)
            return render(
                request,
                "ui/pages/event_registration.html",
                {"event": event, "team": team},
            )

        form = EventRegistrationForm(event=event, account=request.user.account)
        return render(
            request, "ui/pages/event_registration.html", {"event": event, "form": form}
        )

    def post(self, request, event_slug):
        event = get_object_or_404(
            Event.objects.get_listed_events(), slug=event_slug, allow_registration=True
        )
        if not request.user.is_authenticated:
            return redirect(request.path)

        if event.is_account_registered(request.user.account):
            return redirect(request.path)

        form = EventRegistrationForm(
            event=event, account=request.user.account, data=request.POST
        )
        if not form.is_valid():
            return render(
                request,
                "ui/pages/event_registration.html",
                {"event": event, "form": form},
            )

        team = form.save()  # Creates Team object
        services.slack.SlackClient().send_message(
            f'<https://github.com/{request.user.username}|{request.user.username}> registered for {event.name} as "{team.name}"'
        )

        return redirect(request.path)


class SettingsView(LoginRequiredMixin, View):
    def get(self, request):
        account = get_object_or_404(Account, user=request.user)
        form = AccountForm(instance=account)

        return render(
            request,
            "ui/pages/account_settings.html",
            {"form": form, "account": account},
        )

    def post(self, request):
        account = get_object_or_404(Account, user=request.user)
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Account updated!")
            return redirect("u", account.user.username)
        return render(
            request,
            "ui/pages/account_settings.html",
            {"form": form, "account": account},
            status=400,
        )
