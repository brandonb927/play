# Generated by Django 2.1.7 on 2019-05-08 18:29

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_game_engine_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='board_settings',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]