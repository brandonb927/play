# Generated by Django 2.2.4 on 2019-08-20 04:09

import apps.common.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("authentication", "0005_data_20190819_2321")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=apps.common.fields.ShortUUIDField(
                max_length=128, prefix="usr", primary_key=True, serialize=False
            ),
        )
    ]
