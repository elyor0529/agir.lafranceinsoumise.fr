# Generated by Django 2.0.9 on 2018-10-17 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0054_auto_20181009_2018")]

    operations = [
        migrations.AddField(
            model_name="eventsubtype",
            name="allow_external",
            field=models.BooleanField(
                default=False, verbose_name="Les non-insoumis⋅es peuvent rejoindre"
            ),
        )
    ]
