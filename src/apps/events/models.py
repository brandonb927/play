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

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(
        default="", blank=True, help_text="This field supports Markdown."
    )

    date = models.DateField(default=util.time.today, null=True, blank=True)
    location = models.CharField(max_length=100, default="", blank=True)
    registration_url = models.URLField(default="", blank=True)

    is_listed = models.BooleanField(default=False, null=False)

    objects = EventManager()

    def is_upcoming(self):
        return not self.date or self.date >= util.time.today()


class Team(BaseModel):
    id = ShortUUIDField(prefix="team_", max_length=128, primary_key=True)

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    accounts = models.ManyToManyField(Account)
    snake = models.ForeignKey(Snake, on_delete=models.DO_NOTHING)

    bio = models.TextField(default="", blank=True)
    profile_pic_url = models.URLField(default="", blank=True)
    profile_pic_approved = models.BooleanField(default=False)
