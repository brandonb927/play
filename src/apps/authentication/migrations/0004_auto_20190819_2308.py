# Generated by Django 2.2.4 on 2019-08-19 23:08

import apps.common.fields
from django.db import migrations
import util.time


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_user_is_commentator'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created',
            field=apps.common.fields.CreatedDateTimeField(blank=True, default=util.time.now, editable=False),
        ),
        migrations.AddField(
            model_name='user',
            name='modified',
            field=apps.common.fields.ModifiedDateTimeField(blank=True, default=util.time.now, editable=False),
        ),
    ]
