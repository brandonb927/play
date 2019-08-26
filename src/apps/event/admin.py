from django.contrib import admin

from apps.event.models import Event
from apps.common.models import BaseModelAdmin


@admin.register(Event)
class EventAdmin(BaseModelAdmin):
    readonly_fields = BaseModelAdmin.readonly_fields + ("id",)
    list_display = ("name", "date", "location", "is_listed")
    ordering = ("date",)
