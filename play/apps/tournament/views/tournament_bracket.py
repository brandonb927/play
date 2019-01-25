import csv

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from apps.tournament.forms import TournamentBracketForm
from apps.tournament.models import TournamentBracket, Heat, HeatGame
from apps.authentication.decorators import admin_required


@admin_required
@login_required
@transaction.atomic
def new(request):
    if request.method == 'POST':
        form = TournamentBracketForm(request.POST)

        if form.is_valid():
            tournament = form.save()
            messages.success(request, f'Tournament "{tournament.name}" successfully created')
            return redirect('/tournaments/')
    else:
        form = TournamentBracketForm()

    return render(request, 'tournament_bracket/new.html', { 'form': form })


@admin_required
@login_required
def edit(request, id):
    tournament_bracket = TournamentBracket.objects.get(id=id)
    if request.method == 'POST':
        form = TournamentBracketForm(request.POST, instance=tournament_bracket)

        if form.is_valid():
            form.save()
            messages.success(request, f'Tournament Bracket "{tournament_bracket.name}" updated')
            return redirect('/tournaments/')
    else:
        form = TournamentBracketForm(instance=tournament_bracket)

    return render(request, 'tournament_bracket/edit.html', {'form': form})


@admin_required
@login_required
def show_current_game(request, id):
    tournament_bracket = TournamentBracket.objects.get(id=id)

    if request.GET.get("json") == 'true':
        details = tournament_bracket.game_details()
        return JsonResponse({"games": details})

    return render(request, 'tournament_bracket/show_current_game.html', {
        'tournament_bracket': tournament_bracket,
    })

@admin_required
@login_required
def show(request, id):
    tournament_bracket = TournamentBracket.objects.get(id=id)
    return render(request, 'tournament_bracket/show.html', {
        'tournament_bracket': tournament_bracket,
    })


@admin_required
@login_required
def show_csv(request, id):
    tournament_bracket = TournamentBracket.objects.get(id=id)
    # Create the HttpResponse object with the appropriate CSV header.
    filename = f'{tournament_bracket.tournament.name}_{tournament_bracket.name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    for row in tournament_bracket.export():
        writer.writerow(row)

    return response


@admin_required
@login_required
def create_next_round(request, id):
    tournament_bracket = TournamentBracket.objects.get(id=id)
    try:
        tournament_bracket.create_next_round()
    except:
        messages.error(request, f"Failed to create a new tournament round")

    return redirect(f'/tournament/bracket/{id}')


@admin_required
@login_required
def create_game(request, id, heat_id):
    heat = Heat.objects.get(id=heat_id)
    try:
        heat.create_next_game()
    except:
        messages.error(request, f"Failed to add a new bracket heat")
    return redirect(f'/tournament/bracket/{id}/')


@admin_required
@login_required
def run_game(request, id, heat_id, heat_game_number):
    heat_game = HeatGame.objects.get(heat_id=heat_id, number=heat_game_number)
    if heat_game.game is None or heat_game.game.engine_id is None:
        heat_game.game.create()
        heat_game.game.run()
    return redirect(f'/games/{heat_game.game.engine_id}')