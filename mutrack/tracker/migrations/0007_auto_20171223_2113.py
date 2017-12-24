# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-24 05:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_auto_20171203_1621'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'ordering': ('-rating', 'artist', 'name')},
        ),
        migrations.AlterModelOptions(
            name='artist',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='listen',
            name='listen_date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
    ]
