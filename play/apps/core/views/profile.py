from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, redirect

from apps.core.models import GameSnake, Profile
from apps.core.forms import ProfileForm
from apps.core.middleware import profile_required


@profile_required
def show(request, username):
    # Case-insensitive lookup, redirects to correct URL
    profile = Profile.objects.get(user__username__iexact=username)
    if profile.username != username:
        return redirect("u", profile.username)

    games = (
        profile.games.watchable()
        .order_by("-created")
        .prefetch_related("gamesnake_set__snake")
        .distinct()[:10]
    )

    return render(
        request,
        "core/profile/show.html",
        {
            "profile_image": True,
            "profile_description": f"{profile.username} on Battlesnake!",
            "profile": profile,
            "games": games,
        },
    )


@profile_required
def show_by_game_snake(request, game_snake_id):
    try:
        game_snake = GameSnake.objects.get(id=game_snake_id)
    except GameSnake.DoesNotExist:
        raise Http404
    return redirect("u", game_snake.snake.profile.username)


@login_required
def edit(request):
    profile, is_new_profile = Profile.objects.get_or_init(user=request.user)
    form = ProfileForm(instance=profile)
    return render(
        request,
        "core/profile/edit.html",
        {"form": form, "profile": profile, "show_activation": is_new_profile},
    )


@login_required
def update(request):
    profile, is_new_profile = Profile.objects.get_or_init(user=request.user)
    form = ProfileForm(request.POST, instance=profile)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO, "Account settings updated")
        return redirect("u", profile.username)
    return render(
        request,
        "core/profile/edit.html",
        {"form": form, "profile": profile, "show_activation": is_new_profile},
        status=400,
    )


@login_required
@profile_required
@transaction.atomic
def delete(request):
    user = request.user
    logout(request)
    user.delete()
    if hasattr(user, "profile"):
        user.profile.delete()
    return redirect("/")
