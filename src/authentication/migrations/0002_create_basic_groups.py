# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-09 13:47
from __future__ import unicode_literals

from django.db import migrations


def create_basic_groups(apps, schema):
    Permission = apps.get_model("auth", "Permission")
    Group = apps.get_model("auth", "Group")

    oauth_providers_permissions = [
        'view_person',
        'add_authorization',
        'change_authorization',
        'delete_authorization',
        'view_client',
    ]

    workers_permissions = [
        'add_person', 'change_person', 'view_person',
        'add_persontag', 'change_persontag', 'delete_persontag',
        'add_calendar', 'change_calendar', 'delete_calendar',
        'add_event', 'change_event',
        'add_eventtag', 'change_eventtag', 'delete_eventtag',
        'add_rsvp', 'change_rsvp', 'delete_rsvp', 'view_rsvp',
        'add_membership', 'change_membership', 'delete_membership', 'view_membership',
        'add_supportgroup', 'change_supportgroup',
        'add_supportgrouptag', 'change_supportgrouptag', 'delete_supportgrouptag',
    ]

    oauth_providers = Group.objects.create(name='oauth_providers')
    oauth_providers.permissions.add(*Permission.objects.filter(codename__in=oauth_providers_permissions))

    workers = Group.objects.create(name='workers')
    workers.permissions.add(*Permission.objects.filter(codename__in=workers_permissions))


def delete_basic_groups(apps, schema):
    Group = apps.get_model("auth", "Group")

    Group.objects.filter(name__in=['oauth_providers', 'workers']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0001_initial'),
        # depends on auth models to be created
        ('auth', '0008_alter_user_username_max_length'),
        # depends on needed permissions actually existing
        ('events', '0001_initial'),
        ('groups', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_basic_groups, delete_basic_groups, atomic=True)
    ]
