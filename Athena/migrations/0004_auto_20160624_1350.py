# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-24 13:50
from __future__ import unicode_literals

import Athena.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Athena', '0003_auto_20160623_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atividade',
            name='arquivo_entrada2',
            field=models.FileField(default=None, upload_to=Athena.models.atividade_path),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='arquivo_roteiro',
            field=models.FileField(default=None, upload_to=Athena.models.atividade_path),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='arquivo_saida2',
            field=models.FileField(default=None, upload_to=Athena.models.atividade_path),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='arquivo_testador',
            field=models.FileField(default=None, upload_to=Athena.models.atividade_path),
        ),
    ]
