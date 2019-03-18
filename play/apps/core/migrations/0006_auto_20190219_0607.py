# Generated by Django 2.0.10 on 2019-02-19 06:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0005_auto_20190215_0323")]

    operations = [
        migrations.AlterField(
            model_name="snake",
            name="name",
            field=models.CharField(
                max_length=128,
                validators=[
                    django.core.validators.MinLengthValidator(3),
                    django.core.validators.MaxLengthValidator(50),
                ],
            ),
        )
    ]
