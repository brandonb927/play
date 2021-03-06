# Generated by Django 2.2.4 on 2019-08-24 00:23

import apps.common.fields
from django.db import migrations, models
import django.db.models.deletion
import util.time


class Migration(migrations.Migration):

    dependencies = [("core", "0017_delete_profile")]

    operations = [
        migrations.CreateModel(
            name="ContentReport",
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
                        max_length=128, prefix=None, primary_key=True, serialize=False
                    ),
                ),
                ("url", models.CharField(default="", max_length=200)),
                ("text", models.TextField(default="")),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="core.Account",
                    ),
                ),
            ],
            options={"abstract": False},
        )
    ]
