# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-22 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Athena', '0003_auto_20160508_0121'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividade',
            name='restricoes',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]