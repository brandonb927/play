# Generated by Django 2.2.4 on 2019-08-22 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20190820_0409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_commentator',
        ),
    ]
