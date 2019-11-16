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
    raw_id_fields = ("accounts",)  # For Performance

    list_display = ("name", "get_event_display", "division")
    list_filter = ("division",)
    ordering = ("name",)
    search_fields = ("name", "division")

    def get_event_display(self, obj):
        return obj.event.name

    get_event_display.short_description = "Event"
