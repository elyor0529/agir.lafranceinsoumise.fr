# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-21 07:29
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_auto_20170615_0849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authorization',
            name='scopes',
        ),
        migrations.AddField(
            model_name='authorization',
            name='scopes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('view_profile', 'Voir mon profil'), ('edit_profile', 'Changer mon profil'), ('edit_event', 'Éditer mes événements'), ('edit_rsvp', 'Voir et éditer mes participations aux événements'), ('edit_supportgroup', "Éditer mes groupes d'appui"), ('edit_membership', "Voir et éditer mes participations aux groups d'appui"), ('edit_authorization', "Éditer mes autorisations d'accès")], max_length=255), blank=True, default=list, help_text='La liste des scopes autorisés.', size=None),
        ),
        migrations.RemoveField(
            model_name='client',
            name='scopes',
        ),
        migrations.AddField(
            model_name='client',
            name='scopes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('view_profile', 'Voir mon profil'), ('edit_profile', 'Changer mon profil'), ('edit_event', 'Éditer mes événements'), ('edit_rsvp', 'Voir et éditer mes participations aux événements'), ('edit_supportgroup', "Éditer mes groupes d'appui"), ('edit_membership', "Voir et éditer mes participations aux groups d'appui"), ('edit_authorization', "Éditer mes autorisations d'accès")], max_length=255), blank=True, default=list, help_text='La liste des scopes autorisés pour ce client.', size=None),
        ),
        migrations.DeleteModel(
            name='Scope',
        ),
    ]