import logging

from django.db import models

from apps.common.fields import ShortUUIDField
from apps.common.models import BaseManager, BaseModel
from apps.core.models import Account, Snake
import util.time


logger = logging.getLogger(__name__)


class EventManager(BaseManager):
    def get_listed_events(self):
        return self.get_queryset().filter(is_listed=True)


class Event(BaseModel):
    id = ShortUUIDField(prefix="evt", max_length=128, primary_key=True)

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    tldr = models.TextField(
        default="", blank=True, help_text="This field supports Markdown."
    )
    description = models.TextField(
        default="", blank=True, help_text="This field supports Markdown."
    )

    date = models.DateField(default=util.time.today, null=True, blank=True)
    location = models.CharField(max_length=100, default="", blank=True)
    banner_image_url = models.URLField(default="", blank=True)

    allow_registration = models.BooleanField(default=False)
    is_listed = models.BooleanField(default=False, null=False)

    objects = EventManager()

    def is_account_registered(self, account):
        return Team.objects.filter(event=self, accounts=account).exists()

    def is_upcoming(self):
        return not self.date or self.date >= util.time.today()


class TeamManager(BaseManager):
    pass


class Team(BaseModel):
    class Meta:
        unique_together = ("event", "name")

    id = ShortUUIDField(prefix="team", max_length=128, primary_key=True)

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    accounts = models.ManyToManyField(Account)
    snake = models.ForeignKey(Snake, on_delete=models.DO_NOTHING)

    # bvanvugt: This is jankily hardcoded for now
    DIVISION_CHOICES = [("Rookie", "Rookie"), ("Veteran", "Veteran")]
    division = models.CharField(max_length=32, choices=DIVISION_CHOICES)

    bio = models.TextField(default="", blank=True)
    profile_pic_url = models.URLField(default="", blank=True)
    profile_pic_approved = models.BooleanField(default=False)

    objects = TeamManager()
