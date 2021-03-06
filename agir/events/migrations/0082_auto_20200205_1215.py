# Generated by Django 2.2.8 on 2020-02-05 11:15

import agir.lib.form_fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("events", "0081_auto_20200205_1134")]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="legal",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True,
                default=dict,
                encoder=agir.lib.form_fields.CustomJSONEncoder,
                verbose_name="Informations juridiques",
            ),
        )
    ]
