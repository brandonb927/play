# Generated by Django 2.2.4 on 2019-10-17 17:04

import apps.common.fields
from django.db import migrations, models
import util.time


class Migration(migrations.Migration):

    initial = True

    dependencies = [("jobs", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="JobPost",
            fields=[
                (
                    "created",
                    apps.common.fields.CreatedDateTimeField(
                        blank=True, default=util.time.now, editable=False
                    ),
                ),
                (
                    "modified",
                    apps.common.fields.ModifiedDateTimeField(
                        blank=True, default=util.time.now, editable=False
                    ),
                ),
                (
                    "id",
                    apps.common.fields.ShortUUIDField(
                        max_length=128, prefix="job", primary_key=True, serialize=False
                    ),
                ),
                ("role", models.CharField(max_length=100)),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="This field supports Markdown.",
                    ),
                ),
            ],
            options={"abstract": False},
        )
    ]
