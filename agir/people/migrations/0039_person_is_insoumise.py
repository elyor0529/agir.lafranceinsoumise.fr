# Generated by Django 2.0.9 on 2018-10-10 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0038_contact_phone_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_insoumise',
            field=models.BooleanField(default=True, verbose_name='Insoumis⋅e'),
        ),
    ]