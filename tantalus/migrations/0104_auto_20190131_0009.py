# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-01-31 00:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tantalus', '0103_auto_20190123_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultsdataset',
            name='libraries',
            field=models.ManyToManyField(blank=True, to='tantalus.DNALibrary'),
        ),
        migrations.AlterField(
            model_name='resultsdataset',
            name='samples',
            field=models.ManyToManyField(blank=True, to='tantalus.Sample'),
        ),
    ]
