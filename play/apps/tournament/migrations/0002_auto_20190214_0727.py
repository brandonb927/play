# Generated by Django 2.0.10 on 2019-02-14 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("tournament", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="description",
            field=models.TextField(verbose_name="Back Story"),
        )
    ]
