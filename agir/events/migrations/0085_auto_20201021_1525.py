# Generated by Django 3.1.2 on 2020-10-21 13:25

import agir.lib.form_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0084_auto_20200702_1627"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="legal",
            field=models.JSONField(
                blank=True,
                default=dict,
                encoder=agir.lib.form_fields.CustomJSONEncoder,
                verbose_name="Informations juridiques",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="payment_parameters",
            field=models.JSONField(
                blank=True, null=True, verbose_name="Paramètres de paiement"
            ),
        ),
        migrations.AlterField(
            model_name="eventsubtype",
            name="config",
            field=models.JSONField(
                blank=True, default=dict, verbose_name="Configuration"
            ),
        ),
    ]
