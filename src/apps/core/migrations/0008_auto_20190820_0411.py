# Generated by Django 2.2.4 on 2019-08-20 04:11

import apps.common.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("core", "0007_game_engine_url")]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="id",
            field=apps.common.fields.ShortUUIDField(
                max_length=128, prefix="gam", primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="gamesnake",
            name="id",
            field=apps.common.fields.ShortUUIDField(
                max_length=128, prefix="gs", primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="snake",
            name="id",
            field=apps.common.fields.ShortUUIDField(
                max_length=128, prefix="snk", primary_key=True, serialize=False
            ),
        ),
    ]