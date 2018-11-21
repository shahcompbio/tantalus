# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-20 23:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tantalus', '0078_auto_20181120_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileresource',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, help_text='When the file resource was last updated.'),
        ),
        migrations.AddField(
            model_name='historicalfileresource',
            name='last_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(1960, 1, 1, 0, 0), editable=False, help_text='When the file resource was last updated.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalsequencedataset',
            name='last_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(1960, 1, 1, 0, 0), editable=False, help_text='When the dataset was last updated.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sequencedataset',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, help_text='When the dataset was last updated.'),
        ),
    ]