# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-03-30 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tantalus', '0112_auto_20190312_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsequencinglane',
            name='lane_number',
            field=models.CharField(blank=True, choices=[('', ''), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')], max_length=50),
        ),
        migrations.AlterField(
            model_name='sequencinglane',
            name='lane_number',
            field=models.CharField(blank=True, choices=[('', ''), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')], max_length=50),
        ),
    ]
