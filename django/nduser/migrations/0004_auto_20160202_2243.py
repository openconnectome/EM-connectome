# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-03 03:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nduser', '0003_histogram'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='mdengine',
            field=models.CharField(choices=[(b'MySQL', b'MySQL')], default=b'MySQL', max_length=255),
        ),
        migrations.AlterField(
            model_name='project',
            name='host',
            field=models.CharField(choices=[(b'dsp061.pha.jhu.edu', b'default'), (b'dsp061.pha.jhu.edu', b'dsp061'), (b'dsp062.pha.jhu.edu', b'dsp062'), (b'dsp063.pha.jhu.edu', b'dsp063'), (b'localhost', b'Debug')], default=b'dsp061.pha.jhu.edu', max_length=255),
        ),
        migrations.AlterField(
            model_name='project',
            name='kvengine',
            field=models.CharField(choices=[(b'MySQL', b'MySQL'), (b'Cassandra', b'Cassandra'), (b'Riak', b'Riak'), (b'DynamoDB', b'DynamoDB'), (b'Redis', b'Redis')], default=b'MySQL', max_length=255),
        ),
        migrations.AlterField(
            model_name='project',
            name='kvserver',
            field=models.CharField(choices=[(b'dsp061.pha.jhu.edu', b'default'), (b'dsp061.pha.jhu.edu', b'dsp061'), (b'dsp062.pha.jhu.edu', b'dsp062'), (b'dsp063.pha.jhu.edu', b'dsp063'), (b'localhost', b'Debug')], default=b'dsp061.pha.jhu.edu', max_length=255),
        ),
        migrations.AlterField(
            model_name='project',
            name='nd_version',
            field=models.CharField(default=b'0.7', max_length=255),
        ),
        migrations.AlterField(
            model_name='project',
            name='schema_version',
            field=models.CharField(default=b'0.7', max_length=255),
        ),
    ]