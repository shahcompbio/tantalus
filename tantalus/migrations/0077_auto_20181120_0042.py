# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-20 00:42
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tantalus', '0076_auto_20181120_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='version',
            field=models.CharField(default='v0.0.0', max_length=200, validators=[django.core.validators.RegexValidator(message=' must be in "v<MAJOR>.<MINOR>.<PATCH>"; for example, "v0.0.1"', regex='v\\d+\\.\\d+\\.\\d+')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalanalysis',
            name='version',
            field=models.CharField(default='v0.0.0', max_length=200, validators=[django.core.validators.RegexValidator(message=' must be in "v<MAJOR>.<MINOR>.<PATCH>"; for example, "v0.0.1"', regex='v\\d+\\.\\d+\\.\\d+')]),
            preserve_default=False,
        ),
    ]
