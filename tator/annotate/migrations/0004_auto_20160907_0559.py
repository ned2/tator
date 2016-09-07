# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-07 05:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('annotate', '0003_auto_20160907_0553'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='annotation',
            unique_together=set([('query', 'user')]),
        ),
    ]