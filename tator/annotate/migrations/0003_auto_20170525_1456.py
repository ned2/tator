# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-25 14:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0002_auto_20170525_0518'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skipped',
            old_name='comment',
            new_name='description',
        ),
    ]
