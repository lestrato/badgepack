# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-12 21:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badge', '0006_auto_20161112_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badgeclass',
            name='image',
            field=models.ImageField(default='/uploadimage.png', upload_to='uploads/badges/'),
        ),
    ]
