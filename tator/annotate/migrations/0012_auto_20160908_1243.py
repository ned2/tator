# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-08 12:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0011_auto_20160908_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='is_geo_impl',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], verbose_name='isGEOImpl'),
        ),
    ]
