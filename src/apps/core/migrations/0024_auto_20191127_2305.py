# Generated by Django 2.2.4 on 2019-11-27 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0023_auto_20191127_1920"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="profile_slug",
            field=models.SlugField(unique=True),
        ),
    ]