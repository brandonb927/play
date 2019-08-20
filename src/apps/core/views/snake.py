from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.core.forms import SnakeForm
from apps.core.models import Snake


def show(request, snake_id):
    snake = Snake.objects.get(id=snake_id)
    games = (
        snake.games.watchable()
        .order_by("-created")
        .prefetch_related("gamesnake_set__snake")[:10]
    )
    return render(request, "core/snake/show.html", {"snake": snake, "games": games})


@login_required
def new(request):
    form = SnakeForm(request.user.account)
    return render(request, "core/snake/new.html", {"form": form})


@login_required
def create(request):
    form = SnakeForm(request.user.account, request.POST)
    if form.is_valid():
        snake = form.save()
        messages.add_message(
            request, messages.SUCCESS, f"{snake.name} created successfully"
        )
        return redirect(f"/u/{request.user.username}")
    return render(request, "core/snake/edit.html", {"form": form})


@login_required
def edit(request, snake_id):
    try:
        snake = request.user.account.snakes.get(id=snake_id)
        form = SnakeForm(request.user.account, instance=snake)
        return render(request, "core/snake/edit.html", {"form": form})
    except Snake.DoesNotExist:
        return redirect(f"/s/{snake_id}")


@login_required
def update(request, snake_id):
    snake = request.user.account.snakes.get(id=snake_id)
    form = SnakeForm(request.user.account, request.POST, instance=snake)
    if form.is_valid():
        snake = form.save()
        messages.add_message(
            request, messages.SUCCESS, f"{snake.name} updated successfully"
        )
        return redirect(f"/u/{request.user.username}")
    return render(request, "core/snake/edit.html", {"form": form})


@login_required
def delete(request, snake_id):
    snake = request.user.account.snakes.get(id=snake_id)
    snake.delete()
    messages.add_message(
        request, messages.SUCCESS, f"{snake.name} deleted successfully"
    )
    return redirect(f"/u/{request.user.username}")
