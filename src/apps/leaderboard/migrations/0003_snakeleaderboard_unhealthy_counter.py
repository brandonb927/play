# Generated by Django 2.1.7 on 2019-06-10 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("leaderboard", "0002_gameleaderboard_ranked")]

    operations = [
        migrations.AddField(
            model_name="snakeleaderboard",
            name="unhealthy_counter",
            field=models.IntegerField(null=True),
        )
    ]
