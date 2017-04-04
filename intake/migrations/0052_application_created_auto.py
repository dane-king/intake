# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-24 18:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0051_backfill_updated_created_on_applications'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='was_transferred_out',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='application',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]