# Generated by Django 2.2.4 on 2019-11-08 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("events", "0007_auto_20191108_0500")]

    operations = [
        migrations.AlterUniqueTogether(name="team", unique_together={("event", "name")})
    ]