# Generated by Django 2.2.4 on 2019-10-17 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("jobs", "0002_jobpost")]

    operations = [
        migrations.AlterModelOptions(
            name="jobpost", options={"verbose_name": "Job Post"}
        ),
        migrations.AddField(
            model_name="jobpost",
            name="short_description",
            field=models.CharField(blank="True", default="", max_length=1024),
        ),
    ]
