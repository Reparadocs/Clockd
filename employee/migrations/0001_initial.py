# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('unique', models.IntegerField()),
                ('hourly_rate', models.IntegerField()),
                ('logged_in', models.BooleanField(default=False)),
                ('employer', models.ForeignKey(to='employer.Employer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_in', models.DateTimeField()),
                ('current', models.BooleanField(default=True)),
                ('time_out', models.DateTimeField(null=True, blank=True)),
                ('pay', models.IntegerField(default=0)),
                ('employee', models.ForeignKey(to='employee.Employee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
