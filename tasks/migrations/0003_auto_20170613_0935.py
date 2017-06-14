# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0002_auto_20170612_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assigned_to',
            field=models.ForeignKey(related_name='assigned_to', blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=None),
        ),
        migrations.AddField(
            model_name='task',
            name='completed_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='task',
            name='due_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
