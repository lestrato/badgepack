# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-22 16:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0005_auto_20161021_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='accepted_on',
        ),
        migrations.RemoveField(
            model_name='invitation',
            name='accepted_on',
        ),
    ]
