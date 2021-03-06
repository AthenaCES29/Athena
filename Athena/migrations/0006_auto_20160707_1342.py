# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-07 13:42
from __future__ import unicode_literals

import Athena.models
from django.db import migrations, models
import django_dropbox.storage


class Migration(migrations.Migration):

    dependencies = [
        ('Athena', '0005_atividade_teste_publico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atividade',
            name='arquivo_entrada',
            field=models.FileField(default=None, null=True, storage=django_dropbox.storage.DropboxStorage(), upload_to=Athena.models.atividade_path),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='arquivo_entrada2',
            field=models.FileField(default=None, null=True, storage=django_dropbox.storage.DropboxStorage(), upload_to=Athena.models.atividade_path),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='arquivo_roteiro',
            field=models.FileField(default=None, null=True, storage=django_dropbox.storage.DropboxStorage(), upload_to=Athena.models.atividade_path),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='arquivo_saida',
            field=models.FileField(default=None, null=True, storage=django_dropbox.storage.DropboxStorage(), upload_to=Athena.models.atividade_path),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='arquivo_saida2',
            field=models.FileField(default=None, null=True, storage=django_dropbox.storage.DropboxStorage(), upload_to=Athena.models.atividade_path),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='arquivo_testador',
            field=models.FileField(default=None, null=True, storage=django_dropbox.storage.DropboxStorage(), upload_to=Athena.models.atividade_path),
        ),
        migrations.AlterField(
            model_name='submissao',
            name='arquivo_codigo',
            field=models.FileField(default=None, null=True, storage=django_dropbox.storage.DropboxStorage(), upload_to=Athena.models.submissao_path),
        ),
    ]
