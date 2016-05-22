#!/usr/bin/python
# -*- coding: utf-8 -*-

from Athena.models import Aluno, Atividade, Professor, Turma, \
    Submissao, RelAlunoAtividade

from django.contrib import auth
from django.http import JsonResponse


def login(request):

    if request.method == 'GET':
        username = request.GET.get('username', '')
        password = request.GET.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({'valido': False})
        else:

            aluno = Aluno.objects.filter(user=user).first()
            professor = Professor.objects.filter(user=user).first()
            if aluno is not None:
                aluno_json = {}
                aluno_json['id'] = aluno.Id
                aluno_json['valido'] = user.is_authenticated()
                aluno_json = dict(
                    aluno_json.items() +
                    aluno.json_data().items()
                )
                return JsonResponse(aluno_json)
            elif professor is not None:

                professor_json = {}
                professor_json['id'] = professor.Id
                professor_json['valido'] = user.is_authenticated()
                professor_json = dict(
                    professor_json.items() +
                    professor.json_data().items()
                )
                return JsonResponse(professor_json)

    return JsonResponse({'valido': False})


def atividades(request):

    if request.method == 'GET':

        userId = request.GET.get('id', '')

        aluno = Aluno.objects.filter(Id=userId).first()
        professor = Professor.objects.filter(Id=userId).first()

        if aluno is not None:

            atividades_json = {}
            atividades_buf = []

            for relAlunoAtividade in RelAlunoAtividade.objects.filter(
                    aluno=aluno):
                atividades_buf.append(relAlunoAtividade.aluno_json_data())

            atividades_json['valido'] = True
            atividades_json['atividades'] = atividades_buf
            return JsonResponse(atividades_json)
        elif professor is not None:

            atividades_json = {}

            turmas_buf = []
            turmas = Turma.objects.filter(professor=professor)
            for turma in turmas:
                turma_info = {}
                turma_info['id'] = turma.Id
                turma_info['nome'] = turma.nome

                atividades_buf = []
                atividades = Atividade.objects.filter(turma=turma)
                for atividade in atividades:
                    atividades_buf.append(
                        dict(atividade.prof_json_data().items()))

                turma_info['atividades'] = atividades_buf
                turmas_buf.append(dict(turma_info.items()))

            atividades_json['valido'] = True
            atividades_json['turmas'] = turmas_buf
            return JsonResponse(atividades_json)

    return JsonResponse({'valido': False})


def notas(request):

    if request.method == 'GET':

        # Get aluno in db

        userId = request.GET.get('id', '')
        aluno = Aluno.objects.filter(Id=userId).first()

    if aluno is not None:
        notas_json = {}
        notas_buf = []

        # Iterate over submissoes

        submissoes = Submissao.objects.filter(aluno=aluno)
        for submissao in submissoes:
            nota_json = {}
            nota_json['fechada'] = submissao.atividade.estaFechada()
            nota_json['turma'] = submissao.atividade.turma.nome
            nota_json['atividade'] = submissao.atividade.nome
            nota_json['nota'] = submissao.nota
            nota_json['resultado'] = submissao.resultado
            nota_json['data_envio'] = submissao.data_envio
            nota_json['prazo'] = submissao.atividade.data_limite
            notas_buf.append(nota_json)

        notas_json['valido'] = True
        notas_json['notas'] = notas_buf
        return JsonResponse(notas_json)

    return JsonResponse({'valido': False})


def calendario(request):

    if request.method == 'GET':

        # Get aluno in db

        userId = request.GET.get('id', '')
        aluno = Aluno.objects.filter(Id=userId).first()

        if aluno is not None:
            calendario_json = {}
            calendarioAtividade_buf = []

            # Iterate over submissoes

            submissoes = Submissao.objects.filter(aluno=aluno)
            for submissao in submissoes:
                submissao_json = {}
                submissao_json['submetida'] = True
                submissao_json['fechada'] = \
                    submissao.atividade.estaFechada()
                submissao_json['turma'] = submissao.atividade.turma.nome
                submissao_json['atividade'] = submissao.atividade.nome
                submissao_json['data_envio'] = submissao.data_envio
                submissao_json['prazo'] = \
                    submissao.atividade.data_limite
                calendarioAtividade_buf.append(submissao_json)

            for relAlunoAtividade in RelAlunoAtividade.objects.filter(
                    aluno=aluno):
                if not relAlunoAtividade.foiEntregue:
                    atividade_json = {}
                    atividade_json['submetida'] = False
                    atividade_json['fechada'] = \
                        relAlunoAtividade.atividade.estaFechada()
                    atividade_json['turma'] = \
                        relAlunoAtividade.atividade.turma.nome
                    atividade_json['atividade'] = \
                        relAlunoAtividade.atividade.nome
                    atividade_json['prazo'] = \
                        relAlunoAtividade.atividade.data_limite
                    calendarioAtividade_buf.append(atividade_json)

            calendario_json['valido'] = True
            calendario_json['datas'] = calendarioAtividade_buf
            return JsonResponse(calendario_json)

    return JsonResponse({'valido': False})
