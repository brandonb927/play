# Generated by Django 2.2.4 on 2019-11-28 02:02

import apps.common.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0024_auto_20191127_2305"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="profile_slug",
            field=apps.common.fields.LowercaseSlugField(unique=True),
        ),
        migrations.AlterField(
            model_name="account",
            name="source",
            field=models.CharField(blank=True, default="", max_length=30),
        ),
    ]
