# Generated by Django 2.2.4 on 2019-08-19 23:21

from django.db import migrations

import util.time


def forward_migration(apps, schema_editor):
    Profile = apps.get_model("core", "Profile")
    User = apps.get_model("authentication", "User")

    for user in User.objects.all():
        try:
            user.created = user.profile.created
        except Profile.DoesNotExist:
            user.created = util.time.from_unix_timestamp(1546300800)  # Jan 1 2019
        user.save()


def reverse_migration(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0004_auto_20190819_2308"),
        ("core", "0007_game_engine_url"),
    ]

    operations = [migrations.RunPython(forward_migration, reverse_migration)]
