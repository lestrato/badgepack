# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-12 21:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badge', '0007_auto_20161112_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badgeclass',
            name='image',
            field=models.ImageField(upload_to='uploads/badges/'),
        ),
    ]
