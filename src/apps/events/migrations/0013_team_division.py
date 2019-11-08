# Generated by Django 2.2.4 on 2019-11-08 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0012_event_tldr")]

    operations = [
        migrations.AddField(
            model_name="team",
            name="division",
            field=models.CharField(
                choices=[("Rookie", "Rookie"), ("Veteran", "Veteran")],
                default="Rookie",
                max_length=32,
            ),
            preserve_default=False,
        )
    ]
