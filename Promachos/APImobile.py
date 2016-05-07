# -*- coding: utf-8 -*-

import os
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib import auth
from django.template.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from Athena.models import Aluno
from Athena.models import Professor
from Athena.models import Turma
from Athena.models import Atividade
from Athena.models import Submissao
from Athena.models import RelAlunoAtividade
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
                aluno_json['valido'] = user.is_authenticated()
                aluno_json = dict(aluno_json.items() + aluno.json_data().items())
                return JsonResponse(aluno_json)
            
            elif professor is not None:
                professor_json = { }
                professor_json['valido'] = user.is_authenticated()
                professor_json = dict(professor_json.items() + professor.json_data().items())
                return JsonResponse(professor_json)