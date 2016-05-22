#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import zipfile

from Athena.models import Atividade, Submissao
from Athena.models import submissao_path


def notasTurma(turma):
    atividades = Atividade.objects.filter(turma=turma)

    notas_path = 'arquivos/' + turma.path('notas_curso.csv')
    notas = open(notas_path, 'w')

    notas.write(turma.nome + ' - ' + turma.professor.nome + '\n')

    i = 0
    notas.write('Nome')
    for atividade in atividades:
        i = i + 1
        notas.write(';Nota' + str(i))
    notas.write(';Media')

    for aluno in turma.alunos.all():
        media = 0
        notas.write('\n' + aluno.nome + ';')
        for atividade in atividades:
            submissao = Submissao.objects.filter(
                atividade=atividade,
                aluno=aluno
            )
            if submissao:
                submissao = submissao[0]
                notas.write(str(submissao.nota) + ';')
                media = media + submissao.nota
            else:
                notas.write('-;')
        notas.write(str(media / i))
    notas.close()
    return notas


def notasAtividade(atividade):
    notas_path = 'arquivos/' + atividade.path('notas.csv')
    notas = open(notas_path, 'w')
    notas.write(atividade.nome + '\n')
    notas.write('Nome;Enviado;Status;Nota\n')

    # write aluno's notes

    for aluno in atividade.turma.alunos.all():
        submissao = Submissao.objects.filter(
            atividade=atividade,
            aluno=aluno
        )

        notas.write(aluno.nome + ';')
        if submissao:
            submissao = submissao[0]
            notas.write(submissao.data_envio.strftime('%d/%m') + ';')
            notas.write(submissao.resultado + ';')
            notas.write(str(submissao.nota) + ';')
        else:

            notas.write('-;-;-;')

        notas.write('\n')
    notas.close()
    return notas


def zipSubmissoes(atividade):
    arqZip = zipfile.ZipFile(atividade.zip_path(), 'w')
    for aluno in atividade.turma.alunos.all():
        submissoes = Submissao.objects.filter(
            atividade=atividade,
            aluno=aluno
        )
        if submissoes:
            submissao = submissoes.first()
            old_path = 'arquivos/' + submissao_path(submissao,
                                                    os.path.basename(submissao.arquivo_codigo.name))
            new_path = 'arquivos/' + atividade.nome + '_' + aluno.nome \
                + '.c'
            os.rename(old_path, new_path)
            if os.path.isfile(new_path):
                arqZip.write(new_path)
            os.rename(new_path, old_path)

    arqZip.close()
    return arqZip
