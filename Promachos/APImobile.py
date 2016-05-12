# -*- coding: utf-8 -*-

import os
from django import middleware
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib import auth
from django.template.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from Athena.models import Aluno, Professor, Turma, Atividade, Submissao, RelAlunoAtividade
from Athena.utils import checar_login_professor, checar_login_aluno

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
                aluno_json = { }
                aluno_json['id'] = aluno.Id
                aluno_json['valido'] = user.is_authenticated()
                aluno_json = dict(aluno_json.items() + aluno.json_data().items())
                return JsonResponse(aluno_json)
            
            elif professor is not None:
                professor_json = { }
                professor_json['id'] = professor.Id
                professor_json['valido'] = user.is_authenticated()
                professor_json = dict(professor_json.items() + professor.json_data().items())
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

            for relAlunoAtividade in RelAlunoAtividade.objects.filter(aluno=aluno):
                atividades_buf.append(dict(relAlunoAtividade.aluno_json_data().items()))
            
            atividades_json['valido'] = True
            atividades_json['atividades'] = atividades_buf
            return JsonResponse(atividades_json)
            
        elif professor is not None:

            atividades_json = { }

            turmas_buf = []
            turmas = Turma.objects.filter(professor=professor)
            for turma in turmas:
                turma_info = {}
                turma_info['id'] = turma.Id
                turma_info['nome'] = turma.nome

                atividades_buf = []
                atividades = Atividade.objects.filter(turma=turma)
                for atividade in atividades:
                    atividades_buf.append(dict(atividade.prof_json_data().items()))

                turma_info['atividades'] = atividades_buf
                turmas_buf.append(dict(turma_info.items()))

            atividades_json['valido'] = True
            atividades_json['turmas'] = turmas_buf
            return JsonResponse(atividades_json)

    return JsonResponse({'valido': False})


def notas(request):

    return JsonResponse({'valido': False})