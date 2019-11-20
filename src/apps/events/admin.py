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
    list_display = ("name", "display_event_name", "division")
    list_filter = ("division",)
    ordering = ("name",)
    search_fields = ("name", "division")

    readonly_fields = BaseModelAdmin.readonly_fields + ("id",)
    raw_id_fields = ("accounts",)  # For Performance

    def display_event_name(self, obj):
        return obj.event.name

    display_event_name.short_description = "Event"
