# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-13 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tantalus', '0047_auto_20180612_0004'),
    ]

    operations = [
        migrations.AddField(
            model_name='gscwgsbamquery',
            name='skip_older_than',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
