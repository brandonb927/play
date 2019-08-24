from django.contrib import admin
from django.db import models

from apps.common.fields import CreatedDateTimeField, ModifiedDateTimeField


class BaseManager(models.Manager):
    def get_or_init(self, defaults=None, **kwargs):
        try:
            return self.get(**kwargs), False
        except self.model.DoesNotExist:
            defaults = defaults or {}
            defaults.update(kwargs)
            return self.model(**defaults), True


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created = CreatedDateTimeField()
    modified = ModifiedDateTimeField()

    objects = BaseManager()

    def __str__(self):
        return f"{self.__class__.__name__}[{self.id}]"


class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "modified")
