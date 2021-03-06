# Generated by Django 2.2.4 on 2019-08-20 04:12

import apps.common.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import util.time


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0008_auto_20190820_0411"),
    ]

    operations = [
        migrations.CreateModel(
            name="Account",
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
                        max_length=128, prefix="act", primary_key=True, serialize=False
                    ),
                ),
                ("marketing_optin", models.BooleanField(default=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False},
        )
    ]
