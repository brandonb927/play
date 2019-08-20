from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from apps.core.forms import AccountForm
from apps.core.models import Account, Game, GameSnake


@login_required
def edit(request):
    account = Account.objects.get(user=request.user)
    form = AccountForm(instance=account)

    return render(
        request,
        "core/account/edit.html",
        {
            "form": form,
            "account": account,
            "show_activation": False,
        },  # TODO: Remove show_activation
    )


@login_required
def update(request):
    account = Account.objects.get(user=request.user)
    form = AccountForm(request.POST, instance=account)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO, "Account updated!")
        return redirect("u", account.user.username)
    return render(
        request,
        "core/account/edit.html",
        {
            "form": form,
            "account": account,
            "show_activation": False,
        },  # TODO: Remove show_activation
        status=400,
    )


@login_required
def show(request, username):
    # Case-insensitive lookup, redirects to correct URL
    account = Account.objects.get(user__username__iexact=username)
    if account.user.username != username:
        return redirect("u", account.user.username)

    games = (
        Game.objects.filter(snakes__account=account)
        .watchable()
        .order_by("-created")
        .prefetch_related("gamesnake_set__snake")
        .distinct()[:10]
    )

    return render(
        request, "core/account/show.html", {"account": account, "games": games}
    )


@login_required
def show_by_game_snake(request, game_snake_id):
    try:
        game_snake = GameSnake.objects.get(id=game_snake_id)
    except GameSnake.DoesNotExist:
        raise Http404
    return redirect("u", game_snake.snake.account.user.username)
