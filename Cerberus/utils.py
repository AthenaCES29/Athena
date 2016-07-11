#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import zipfile

from Athena.models import Atividade, Submissao


def notasTurma(turma):
    atividades = Atividade.objects.filter(turma=turma)

    notas_path = 'temp/notas_curso.csv'
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
    return open(notas_path, "r")


def notasAtividade(atividade):
    notas_path = 'temp/notas.csv'
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
    return open(notas_path, "r")


def zipSubmissoes(atividade):
    arqZip = zipfile.ZipFile(atividade.zip_path(), 'w')
    for aluno in atividade.turma.alunos.all():
        submissoes = Submissao.objects.filter(
            atividade=atividade,
            aluno=aluno
        )
        if submissoes:
            submissao = submissoes.first()
            code_file = atividade.nome + '_' + aluno.nome + '.c'

            code_buffer = open(code_file, 'w')
            code_buffer.write(submissao.arquivo_codigo.read())
            code_buffer.close()

            arqZip.write(code_file)
            os.remove(code_file)

    arqZip.close()
    return open(atividade.zip_path(), "r")
