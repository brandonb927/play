# Generated by Django 2.0.10 on 2019-02-17 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("tournament", "0005_auto_20190215_0044")]

    operations = [
        migrations.RemoveField(model_name="tournament", name="single_snake_per_team")
    ]
