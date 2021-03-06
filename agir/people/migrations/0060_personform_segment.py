# Generated by Django 2.2.3 on 2019-09-26 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0004_auto_20190918_1530"),
        ("people", "0059_auto_20190902_1210"),
    ]

    operations = [
        migrations.AddField(
            model_name="personform",
            name="segment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="person_forms",
                related_query_name="person_form",
                to="mailing.Segment",
            ),
        )
    ]
