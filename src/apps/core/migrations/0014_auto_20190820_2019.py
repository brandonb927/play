# Generated by Django 2.2.4 on 2019-08-20 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("core", "0013_auto_20190820_2009")]

    operations = [
        migrations.AlterField(
            model_name="snake",
            name="account",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.Account"
            ),
        )
    ]