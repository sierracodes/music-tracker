# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-04 00:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_auto_20171203_1542'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='album',
            unique_together=set([('name', 'artist')]),
        ),
    ]
