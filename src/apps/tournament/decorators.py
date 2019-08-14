from django.shortcuts import redirect

from apps.tournament.models import Team


def with_current_team(action):
    def decorate(request, *args, **kwargs):
        try:
            team = Team.objects.get(team_members=request.user.profile)
            request.team = team
            return action(request, *args, **kwargs)
        except Team.DoesNotExist:
            return redirect("/team/new")

    return decorate
