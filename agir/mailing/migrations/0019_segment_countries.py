# Generated by Django 2.2.8 on 2019-12-13 15:03

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [("mailing", "0018_segment_departements")]

    operations = [
        migrations.AddField(
            model_name="segment",
            name="countries",
            field=django_countries.fields.CountryField(
                blank=True,
                max_length=770,
                multiple=True,
                verbose_name="Limiter aux pays",
            ),
        )
    ]