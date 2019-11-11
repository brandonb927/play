import logging

from django import forms
from django.conf import settings

from apps.core.models import Game, GameSnake
from apps.events.models import Team


logger = logging.getLogger(__name__)


class CreateTournamentGameForm(forms.Form):
    BOARD_WIDTH = 11
    BOARD_HEIGHT = 11
    MAX_TURNS_TO_NEXT_FOOD_SPAWN = 12

    # Input Fields
    title = forms.CharField()
    teams = forms.CharField(widget=forms.Textarea)

    def save(self):
        teams = []
        for team_name in self.cleaned_data["teams"].split("\n"):
            try:
                team = Team.objects.get(name=team_name.strip())
                teams.append(team)
            except Team.DoesNotExist:
                pass

        game = None
        if teams:
            game = Game.objects.create(
                width=self.BOARD_WIDTH,
                height=self.BOARD_HEIGHT,
                max_turns_to_next_food_spawn=self.MAX_TURNS_TO_NEXT_FOOD_SPAWN,
                engine_url=settings.BATTLESNAKE_ENGINE_URL,
            )
            for team in teams:
                game.snakes.add(team.snake)
                GameSnake.objects.create(snake=team.snake, name=team.name, game=game)

            game.save()
            game.create()
            game.run()

        return game
