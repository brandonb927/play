# Generated by Django 2.0.10 on 2019-02-10 06:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

import apps.common.fields
import util.time


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("authentication", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Game",
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
                        max_length=128, primary_key=True, serialize=False
                    ),
                ),
                ("engine_id", models.CharField(max_length=128, null=True)),
                ("status", models.CharField(default="pending", max_length=30)),
                ("turn", models.IntegerField(default=0)),
                ("width", models.IntegerField()),
                ("height", models.IntegerField()),
                ("max_turns_to_next_food_spawn", models.IntegerField(default=15)),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="GameSnake",
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
                        max_length=128, primary_key=True, serialize=False
                    ),
                ),
                ("death", models.CharField(default="pending", max_length=128)),
                ("turns", models.IntegerField(default=0)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.Game"
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Profile",
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
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("optin_marketing", models.BooleanField(default=False)),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Snake",
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
                        max_length=128, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                ("url", models.CharField(max_length=128)),
                (
                    "is_public",
                    models.BooleanField(
                        default=False,
                        verbose_name="Allow anyone to add this snake to a game",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.AddField(
            model_name="gamesnake",
            name="snake",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.Snake"
            ),
        ),
        migrations.AddField(
            model_name="game",
            name="snakes",
            field=models.ManyToManyField(to="core.Snake"),
        ),
    ]
