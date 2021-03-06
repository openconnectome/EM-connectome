# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 22:07
from __future__ import unicode_literals

from django.db import migrations

def insert_sites(apps, schema_editor):
  """Insert site name in django sites"""
  Site = apps.get_model('sites', 'Site')
  Site.objects.all().delete()
  # insert neurodata
  Site.objects.create(domain='cloud.neurodata.io', name='cloud')

class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_sites)
    ]
