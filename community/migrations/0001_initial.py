# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 13:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('tag', models.CharField(max_length=5)),
                ('is_private', models.BooleanField(default=False)),
                ('created_on', models.DateField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'community',
                'verbose_name': 'community',
                'verbose_name_plural': 'communities',
            },
        ),
    ]
