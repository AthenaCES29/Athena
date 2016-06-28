# -*- coding: utf-8 -*-
from itertools import izip_longest

import re

from datetime import datetime

from pprint import pprint

from Aeacus import compare

from Athena.models import Atividade, RelAlunoAtividade, Submissao, Turma
from Athena.utils import checar_login_aluno, checar_login_professor

from Cerberus.forms import AtividadeRegistration, TurmaRegistration, \
    UserRegistrationForm
from Cerberus.utils import notasAtividade, notasTurma, zipSubmissoes

from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf
from django.utils import timezone

from .forms import AtividadeCreationForm, AtividadeEditForm, \
    TurmaCreationForm, UploadFileForm


def login(request):

    professor = checar_login_professor(request)
    aluno = checar_login_aluno(request)

    if professor:
        request.session['last_touch'] = datetime.now()
        return HttpResponseRedirect('/professor')
    if aluno:
        request.session['last_touch'] = datetime.now()
        return HttpResponseRedirect('/aluno')

    if request.method == 'POST':

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            matchObjAluno = re.match(
                r'(.*)@aluno.ita.br$', user.email, re.M | re.I)

            if matchObjAluno:
                return HttpResponseRedirect('/aluno/')
            return HttpResponseRedirect('/professor/')

        else:
            return render_to_response(
                'login.html',
                {
                    "invalid_message": "Login inválido. Tente novamente.",
                    "success_message": ""
                },
                context_instance=RequestContext(request),
            )

    try:
        if request.session['advise'] == 'true':
            request.session['advise'] = 'false'
            return render_to_response(
                'login.html',
                {
                    "invalid_message": "Sessao expirada",
                    "success_message": ""
                },
                context_instance=RequestContext(request),
            )
    except KeyError:
        pass

    return render_to_response(
        'login.html',
        {
            "invalid_message": ""
        },
        context_instance=RequestContext(request))


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response(
                'login.html',
                {
                    "invalid_message": "",
                    "success_message": "O cadastro foi realizado com sucesso!"
                },
                context_instance=RequestContext(request),
            )

    else:
        form = UserRegistrationForm()
    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('cadastro.html', args)


def home(request):

    if request.user.is_authenticated():
        form = UploadFileForm()
        if request.method == 'POST':
            testador = request.FILES.getlist('file')[0]
            entrada = request.FILES.getlist('file')[1]
            entrada2 = request.FILES.getlist('file')[2]
            fonte = request.FILES.getlist('file')[5]

            resultado = compare.mover(
                testador, entrada, entrada2, fonte, []
            )

            return render(
                request, 'teste_juiz.html',
                {
                    'form': form,
                    'resultado': resultado,
                }
            )

        return render(request, 'teste_juiz.html', {'form': form})

    else:
        return HttpResponseRedirect('/login/')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')


def professor(request):

    professor = checar_login_professor(request)

    if not professor:
        return HttpResponseRedirect('/login/')

    professor = professor[0]

    form = TurmaCreationForm()
    if request.method == 'POST':
        pprint(request.POST)
        if('post_turma' in request.POST):
            turma = TurmaRegistration(request)
        elif ('post_atividade' in request.POST):
            atividade = AtividadeRegistration(request)
            turma = Turma.objects.get(id=request.POST['id_turma'])
            for aluno in turma.alunos.all():
                relAlunoAtividade = RelAlunoAtividade(
                    foiEntregue=False,
                    aluno=aluno,
                    atividade=atividade,
                )
                relAlunoAtividade.save()
        elif ('post_deletar' in request.POST):
            turma = Turma.objects.get(id=request.POST['id_turma'])

            atividades = Atividade.objects.filter(turma=turma)

            for atividade in atividades:
                submissoes = Submissao.objects.filter(
                    atividade=atividade,
                )

                for submissao in submissoes:
                    submissao.remove_file()
                submissoes.delete()

                atividade.remove_roteiro()
                atividade.remove_testador()
                atividade.remove_entrada()
                atividade.remove_entrada2()
                atividade.remove_saida()
                atividade.remove_saida2()

            atividades.delete()
            turma.delete()

        elif ('post_down_all_notas' in request.POST):

            # model for notes
            turma = Turma.objects.get(id=request.POST['id_turma'])
            atividades = Atividade.objects.filter(turma=turma)

            # generate .csv file
            notas_path = "arquivos/" + turma.path("notas_curso.csv")
            notasTurma(turma)

            # send the file as http response
            arquivo = open(notas_path, "r")
            response = HttpResponse(arquivo)
            response[
                'Content-Disposition'] = 'attachment; filename=notas_curso.csv'

            return response

    turmas = Turma.objects.filter(professor=professor)
    panes = []
    for turma in turmas:
        atividades = Atividade.objects.filter(turma=turma)
        panes.append(
            render_to_response(
                'pane_professor.html',
                {
                    "turma": turma,
                    "atividades": atividades,
                    "form": AtividadeCreationForm(prefix=turma.id),
                },
                context_instance=RequestContext(request),
            ).content
        )

    return render_to_response(
        'professor.html',
        {
            "professor": professor,
            "turmas": turmas,
            "panes": panes,
            "form": form
        },
        context_instance=RequestContext(request),
    )


def prof_ativ(request, id_ativ):

    professor = checar_login_professor(request)

    if not professor:
        return HttpResponseRedirect('/login/')

    atividade = Atividade.objects.filter(id=id_ativ)
    if not atividade:
        return HttpResponseRedirect('/professor/')

    professor = professor[0]
    atividade = atividade[0]

    if request.method == 'POST':
        pprint(request.POST)
        if('post_edit_atividade' in request.POST):
            atividade.nome = request.POST['nome']
            atividade.descricao = request.POST['descricao']
            atividade.data_limite = request.POST['data_limite']
            atividade.restricoes = request.POST['restricoes']
            if atividade.teste_publico:
                atividade.peso1 = request.POST['peso1']
            if atividade.teste_privado:
                atividade.peso2 = request.POST['peso2']

            files = request.FILES
            for file in files:
                print file
            if 'arquivo_roteiro' in files:
                atividade.arquivo_roteiro = files['arquivo_roteiro']
            if 'testador' in files:
                atividade.testador = files['testador']
            if 'arquivo_entrada' in files:
                atividade.arquivo_entrada = files['arquivo_entrada']
            if 'arquivo_entrada2' in files:
                atividade.arquivo_entrada2 = files['arquivo_entrada2']
            if 'arquivo_saida' in files:
                atividade.arquivo_saida = files['arquivo_saida']
            if 'arquivo_saida2' in files:
                atividade.arquivo_saida2 = files['arquivo_saida2']
            atividade.save()
            atividade = Atividade.objects.get(id=id_ativ)

        if('post_del_ativ' in request.POST):
            submissoes = Submissao.objects.filter(
                atividade=atividade,
            )

            for submissao in submissoes:
                submissao.remove_file()
            submissoes.delete()

            atividade.remove_roteiro()
            atividade.remove_testador()
            atividade.remove_entrada()
            atividade.remove_entrada2()
            atividade.remove_saida()
            atividade.remove_saida2()
            atividade.delete()

            return HttpResponseRedirect('/professor/')

        if('post_down_notas' in request.POST):

            # generate .csv file
            notas_path = "arquivos/" + atividade.path("notas.csv")
            notasAtividade(atividade)

            # send the file as http response
            arquivo = open(notas_path, "r")
            response = HttpResponse(arquivo)
            response['Content-Disposition'] = 'attachment; filename=notas.csv'

            return response

        if ('post_down_submissoes' in request.POST):

            # generate the file
            zipSubmissoes(atividade)

            # send the file as http response
            arquivo = open(atividade.zip_path(), "r")
            response = HttpResponse(arquivo)
            response['Content-Disposition'] = 'attachment; filename=' + \
                atividade.nome + '.zip'
            return response

    status_aluno = []

    for aluno in atividade.turma.alunos.all():
        submissao = Submissao.objects.filter(
            atividade=atividade, aluno=aluno
        )
        if submissao:
            submissao = submissao[0]

            status_aluno.append(
                (
                    aluno.nome,
                    submissao.data_envio,
                    Submissao.statusDict[submissao.resultado],
                    submissao.arquivo_codigo.url,
                    submissao.nota,
                )
            )

        else:
            status = "NE"
            status_aluno.append(
                (aluno.nome, Submissao.statusDict[status], "-")
            )

    return render_to_response(
        'prof_ativ.html',
        {
            "professor": professor,
            "atividade": atividade,
            "status_aluno": status_aluno,
            "form": AtividadeEditForm(instance=atividade),
        },
        context_instance=RequestContext(request),
    )


def aluno(request):

    aluno = checar_login_aluno(request)

    if not aluno:
        return HttpResponseRedirect('/login/')

    aluno = aluno[0]

    turmas = aluno.turma_set.all()
    panes = []
    atividades_pendentes = []

    for turma in turmas:

        tuple_ativ_subm = []
        atividades = Atividade.objects.filter(turma=turma)

        for atividade in atividades:
            submissao = Submissao.objects.filter(
                atividade=atividade,
                aluno=aluno,
            )
            status = "NE"
            if not atividade.estaFechada():
                if not submissao:
                    atividades_pendentes.append(
                        (atividade.data_limite,
                         atividade.turma,
                         atividade.nome)
                    )
            if submissao:
                submissao = submissao[len(submissao) - 1]
                status = Submissao.statusDict[submissao.resultado]
            tuple_ativ_subm.append([
                atividade,
                submissao,
                status
            ])

        panes.append(
            render_to_response(
                'pane_aluno.html',
                {
                    "aluno": aluno,
                    "turma": turma,
                    "tuple_ativ_subm": tuple_ativ_subm
                },
                context_instance=RequestContext(request),
            ).content
        )

    submissoes = Submissao.objects.filter(aluno=aluno)

    ultimas_submissoes = []

    for submissao in submissoes:
        atividade = submissao.atividade
        data_envio = submissao.data_envio
        turma = atividade.turma

        ultimas_submissoes.append((atividade.nome, data_envio, turma.nome))

    return render_to_response(
        'aluno.html',
        {
            "aluno": aluno,
            "turmas": turmas,
            "panes": panes,
            "ultimas_submissoes": ultimas_submissoes,
            "atividades_pendentes": atividades_pendentes,
        },
        context_instance=RequestContext(request),
    )


def aluno_ativ(request, ativ_id):

    aluno = checar_login_aluno(request)

    if not aluno:
        return HttpResponseRedirect('/login/')

    aluno = aluno[0]

    atividade = Atividade.objects.filter(id=ativ_id)
    if not atividade:
        return HttpResponseRedirect('/aluno/')
    atividade = atividade[0]
    resultado = ""

    relAlunoAtividade = RelAlunoAtividade.objects.filter(
        aluno=aluno,
        atividade=atividade
    )
    if relAlunoAtividade:
        relAlunoAtividade = relAlunoAtividade[0]

    lista_saida = []
    rte_ce_error = ""
    if request.method == 'POST':

        entrada = None
        entrada2 = None
        gabarito = None
        gabarito2 = None
        testador = None

        if atividade.teste_customizado:
            atividade.arquivo_testador.open()
            testador = atividade.arquivo_testador.read()
            atividade.arquivo_testador.close()

        if atividade.teste_publico:
            atividade.arquivo_entrada.open()
            entrada = atividade.arquivo_entrada.read()
            atividade.arquivo_entrada.close()

        if atividade.teste_privado:
            atividade.arquivo_entrada2.open()
            entrada2 = atividade.arquivo_entrada2.read()
            atividade.arquivo_entrada2.close()

        if atividade.teste_publico and not atividade.teste_customizado:
            atividade.arquivo_saida.open()
            gabarito = atividade.arquivo_saida.read()
            atividade.arquivo_saida.close()

        if atividade.teste_privado and not atividade.teste_customizado:
            atividade.arquivo_saida2.open()
            gabarito2 = atividade.arquivo_saida2.read()
            atividade.arquivo_saida2.close()

        fonte = request.FILES['arquivo_codigo']

        if atividade.teste_customizado:
            # Logica de teste com arquivo do professor
            lista_saida.append(
                ("Teste com código do professor:",
                    " não há saídas a serem exibidas")
            )
            status, ret = compare.mover2(
                testador, entrada, entrada2, fonte, atividade.restricoes,
                atividade.teste_publico, atividade.teste_privado
            )

            if status == "AC" or status == "AC2":
                nota = ret
            else:
                nota = 0
        elif atividade.teste_privado:
            # Lógica com diff e teste privado
            status, resultadoPrivado = \
                compare.mover(entrada2, gabarito2, fonte, atividade.restricoes)
            statusPriv = status
            status, resultadoPublico = \
                compare.mover(entrada, gabarito, fonte, atividade.restricoes)
            statusPublic = status
            if statusPublic == "AC" and statusPriv == "WA":
                status = "WA2"

            if status == "WA" or status == "AC" or status == "WA2":
                nums = []

                for s in resultadoPublico.split():
                    if s.isdigit():
                        nums.append(int(s))
                lines_gabarito = gabarito.count('\n')
                resultadoPublico = resultadoPublico.split('\n')
                resultadoPublico.pop(0)
                gabarito = gabarito.split('\n')
                for linha in izip_longest(resultadoPublico, gabarito):
                    lista_saida.append(linha)
                if (len(nums) > 0):
                    num_diffs = nums[0]
                else:
                    num_diffs = 0

                nums = []

                for s in resultadoPrivado.split():
                    if s.isdigit():
                        nums.append(int(s))
                lines_gabarito2 = gabarito2.count('\n')
                resultadoPrivado = resultadoPrivado.split('\n')
                resultadoPrivado.pop(0)
                gabarito2 = gabarito2.split('\n')
                if (len(nums) > 0):
                    num_diffs2 = nums[0]
                else:
                    num_diffs2 = 0

                # arquivo privado obrigtorio
                if num_diffs > 0:
                    nota = 0
                else:
                    nota = (
                        ((lines_gabarito - num_diffs) * atividade.peso1) /
                        lines_gabarito +
                        ((lines_gabarito2 - num_diffs2) * atividade.peso2) /
                        lines_gabarito2
                    )
                nota = nota * 100 / (atividade.peso1 + atividade.peso2)
                nota = int(nota)

            else:
                rte_ce_error = resultadoPublico
                nota = 0
        else:
            # Lógica com diff e sem teste privado
            status, resultadoPublico = \
                compare.mover(entrada, gabarito, fonte, atividade.restricoes)

            if status == "WA" or status == "AC":
                nums = []

                for s in resultadoPublico.split():
                    if s.isdigit():
                        nums.append(int(s))
                lines_gabarito = gabarito.count('\n')
                resultadoPublico = resultadoPublico.split('\n')
                resultadoPublico.pop(0)
                gabarito = gabarito.split('\n')
                for linha in izip_longest(resultadoPublico, gabarito):
                    lista_saida.append(linha)
                if (len(nums) > 0):
                    num_diffs = nums[0]
                else:
                    num_diffs = 0

                nota = int(100 * (lines_gabarito - num_diffs)) / lines_gabarito

            else:
                rte_ce_error = resultadoPublico
                nota = 0

        submissoes = Submissao.objects.filter(
            aluno=aluno,
            atividade=atividade,
        )
        for submissao in submissoes:
            submissao.remove_file()
        submissoes.delete()

        submissao = Submissao(
            data_envio=timezone.now().date(),
            arquivo_codigo=request.FILES['arquivo_codigo'],
            resultado=status,
            nota=nota,
            atividade=atividade,
            aluno=aluno,
        )
        submissao.save()

        if relAlunoAtividade:
            relAlunoAtividade.foiEntregue = True
        else:
            relAlunoAtividade = RelAlunoAtividade(
                foiEntregue=True,
                aluno=aluno,
                atividade=atividade,
            )
        relAlunoAtividade.save()

    submissao = Submissao.objects.filter(
        atividade=atividade,
        aluno=aluno
    )
    status = "NE"
    if submissao:
        submissao = submissao[len(submissao) - 1]
        status = submissao.resultado

    pprint(timezone.now().date())

    prazo_valido = True
    if timezone.now().date() > atividade.data_limite:
        prazo_valido = False

    return render_to_response(
        'aluno_ativ.html',
        {
            "aluno": aluno,
            "atividade": atividade,
            "submissao": submissao,
            "prazo_valido": prazo_valido,
            "relAlunoAtividade": relAlunoAtividade,
            "lista_saida": lista_saida,
            "resultado": resultado,
            "status": Submissao.statusDict[status],
            "compilation_error": rte_ce_error,
        },
        context_instance=RequestContext(request),
    )


def aluno_turmas(request):

    aluno = checar_login_aluno(request)

    if not aluno:
        return HttpResponseRedirect('/login/')

    aluno = aluno[0]

    if request.method == 'POST':
        pprint(request.POST)
        if('post_sair' in request.POST):
            turma = Turma.objects.get(id=request.POST['post_sair'])
            aluno.turma_set.remove(turma)
            aluno.save()
        if('post_entrar' in request.POST):
            turma = Turma.objects.get(id=request.POST['post_entrar'])
            aluno.turma_set.add(turma)
            aluno.save()
            atividades = Atividade.objects.filter(turma=turma)
            for atividade in atividades:
                relAlunoAtividade = RelAlunoAtividade(
                    foiEntregue=False,
                    aluno=aluno,
                    atividade=atividade,
                )
                relAlunoAtividade.save()

        return HttpResponseRedirect('/aluno')

    turmas_registradas = aluno.turma_set.all()
    todas_turmas = Turma.objects.all()
    turmas_nao_registradas = todas_turmas.exclude(
        id__in=[turma_check.id for turma_check in turmas_registradas]
    )

    return render_to_response(
        'lista_turmas.html',
        {
            "turmas_registradas": turmas_registradas,
            "turmas_nao_registradas": turmas_nao_registradas,
        },
        context_instance=RequestContext(request),
    )


def perfil(request):
    return render_to_response(
        'perfil.html',
        context_instance=RequestContext(request),
    )
