# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-11-19 22:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trash',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=None, max_length=45),
            preserve_default=False,
        ),
    ]
