# Generated by Django 2.2.4 on 2019-11-08 17:18

import apps.common.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("events", "0009_auto_20191108_1717")]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="id",
            field=apps.common.fields.ShortUUIDField(
                max_length=128, prefix="team", primary_key=True, serialize=False
            ),
        )
    ]