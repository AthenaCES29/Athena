# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-24 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Athena', '0004_auto_20160624_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividade',
            name='teste_publico',
            field=models.BooleanField(default=False),
        ),
    ]
