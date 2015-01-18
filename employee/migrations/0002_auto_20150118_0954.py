# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='time_1',
            field=models.CharField(default='1/10/2015 13:24', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entry',
            name='time_2',
            field=models.CharField(default='1/10/2015 18:02', max_length=30),
            preserve_default=False,
        ),
    ]
