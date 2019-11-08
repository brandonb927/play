from django.contrib import admin

from apps.events.models import Event, Team
from apps.common.models import BaseModelAdmin


@admin.register(Event)
class EventAdmin(BaseModelAdmin):
    readonly_fields = BaseModelAdmin.readonly_fields + ("id",)
    list_display = ("name", "date", "location", "is_listed")
    ordering = ("date",)


@admin.register(Team)
class TeamAdmin(BaseModelAdmin):
    readonly_fields = BaseModelAdmin.readonly_fields + ("id",)
    list_display = ("name", "event")
    ordering = ("name",)
