# Generated by Django 2.2.4 on 2019-11-23 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0013_team_division")]

    operations = [
        migrations.AddField(
            model_name="event",
            name="banner_image_url",
            field=models.URLField(blank=True, default=""),
        )
    ]