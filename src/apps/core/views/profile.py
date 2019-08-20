from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.core.models import Profile
from apps.core.forms import ProfileForm


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
