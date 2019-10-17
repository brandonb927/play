import logging

from django.db import models

from apps.common.fields import ShortUUIDField
from apps.common.models import BaseManager, BaseModel


logger = logging.getLogger(__name__)


class JobPostManager(BaseManager):
    pass


class JobPost(BaseModel):
    class Meta:
        verbose_name = "Job Post"

    id = ShortUUIDField(prefix="job", max_length=128, primary_key=True)

    role = models.CharField(max_length=100)
    short_description = models.CharField(max_length=1024, default="", blank="True")
    description = models.TextField(
        default="", blank=True, help_text="This field supports Markdown."
    )

    objects = JobPostManager()
