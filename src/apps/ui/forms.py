import logging

from django import forms
from django.db.models import Q

from apps.core.models import Account, Game, GameSnake, Snake


logger = logging.getLogger(__name__)


class AccountForm(forms.ModelForm):
    email = forms.CharField(required=True, widget=forms.EmailInput)

    class Meta:
        model = Account
        fields = ["marketing_optin"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].initial = self.instance.user.email

    def save(self, *args, **kwargs):
        account = super().save(*args, **kwargs)
        account.user.email = self.cleaned_data["email"]
        account.user.save()
        return account


class GameForm(forms.Form):
    board_size = forms.ChoiceField(
        choices=[
            ("small", "Small - 7x7"),
            ("medium", "Medium - 11x11"),
            ("large", "Large - 19x19"),
            ("custom", "Custom"),
        ],
        required=True,
        initial="medium",
    )
    width = forms.IntegerField(initial=11, required=False)
    height = forms.IntegerField(initial=11, required=False)
    snakes = forms.CharField(widget=forms.HiddenInput())
    engine_url = forms.CharField(required=False)

    def save(self, user):
        data = self.cleaned_data
        width = data["width"]
        height = data["height"]
        if data["board_size"] == "small":
            width = 7
            height = 7
        elif data["board_size"] == "medium":
            width = 11
            height = 11
        elif data["board_size"] == "large":
            width = 19
            height = 19

        game = Game.objects.create(
            width=width,
            height=height,
            max_turns_to_next_food_spawn=12,
            engine_url=data["engine_url"],
        )
        snake_ids = self.cleaned_data["snakes"].split(",")
        snakes = Snake.objects.filter(Q(id__in=snake_ids)).can_view(user)
        for s in snakes.all():
            game.snakes.add(s)
        for snake_id in snake_ids:
            GameSnake.objects.create(snake=snakes.get(id=snake_id), game=game)
        game.save()
        return game


class SnakeForm(forms.ModelForm):
    class Meta:
        model = Snake
        fields = ["name", "url", "is_public"]

    def __init__(self, account: Account, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.account = account

    def clean(self):
        cleaned_data = super().clean()
        try:
            name = cleaned_data["name"]

            # need to filter here, in case we already have a Account with multiple snakes with the same name
            snakes = self.account.snakes.filter(name=name)
            if self.instance is not None:
                snakes = snakes.exclude(id=self.instance.id)
            if snakes.count() > 0:
                raise forms.ValidationError(
                    f"{self.account.user.username}/{name} already exists."
                )
        except Snake.DoesNotExist:
            pass

    def save(self, commit=True):
        snake = super().save(commit=False)
        snake.account = self.account
        if commit is True:
            snake.save()
        return snake
