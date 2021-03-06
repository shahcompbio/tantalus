# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-19 18:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tantalus', '0026_auto_20180117_0035'),
    ]

    operations = [
        migrations.CreateModel(
            name='BCLFolder',
            fields=[
                ('abstractdataset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tantalus.AbstractDataSet')),
            ],
            options={
                'abstract': False,
            },
            bases=('tantalus.abstractdataset',),
        ),
        migrations.CreateModel(
            name='HistoricalBCLFolder',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('abstractdataset_ptr', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tantalus.AbstractDataSet')),
                ('dna_sequences', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tantalus.DNASequences')),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical bcl folder',
            },
        ),
        migrations.AddField(
            model_name='fileresource',
            name='is_folder',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalfileresource',
            name='is_folder',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalbclfolder',
            name='folder',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tantalus.FileResource'),
        ),
        migrations.AddField(
            model_name='historicalbclfolder',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalbclfolder',
            name='polymorphic_ctype',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='bclfolder',
            name='folder',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bcl_folder', to='tantalus.FileResource'),
        ),
    ]
