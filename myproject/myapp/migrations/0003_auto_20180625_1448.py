# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-25 14:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20180625_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_time',
            field=models.DateField(default=datetime.datetime(2018, 6, 24, 14, 48, 37, 167670)),
        ),
    ]