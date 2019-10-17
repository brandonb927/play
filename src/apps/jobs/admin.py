from django.contrib import admin

from apps.common.models import BaseModelAdmin
from apps.jobs.models import JobPost


@admin.register(JobPost)
class JobPostAdmin(BaseModelAdmin):
    readonly_fields = BaseModelAdmin.readonly_fields + ("id",)
    list_display = ("role",)
    ordering = ("role",)
