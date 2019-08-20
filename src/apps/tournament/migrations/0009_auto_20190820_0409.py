# Generated by Django 2.2.4 on 2019-08-20 04:09

import apps.common.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("tournament", "0008_auto_20190819_1951")]

    operations = [
        migrations.AlterField(
            model_name="heat",
            name="id",
            field=apps.common.fields.ShortUUIDField(
                max_length=128, prefix="hea", primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="heatgame",
            name="id",
            field=apps.common.fields.ShortUUIDField(
                max_length=128, prefix="hga", primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="round",
            name="id",
            field=apps.common.fields.ShortUUIDField(
                max_length=128, prefix="rnd", primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="id",
            field=apps.common.fields.ShortUUIDField(
                max_length=128, prefix="tem", primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="tournament",
            name="id",
            field=apps.common.fields.ShortUUIDField(
                max_length=128, prefix="trn", primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="tournamentbracket",
            name="id",
            field=apps.common.fields.ShortUUIDField(
                max_length=128, prefix="tbr", primary_key=True, serialize=False
            ),
        ),
    ]