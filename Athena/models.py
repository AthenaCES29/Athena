# -*- coding: utf-8 -*-
import os

from Athena import settings

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def atividade_path(instance, filename):
    return 'atividades/{prof}/{turma}/{id}/{name}'.format(
        prof=instance.turma.professor.id,
        turma=instance.turma.id,
        id=instance.nome,
        name=filename,
    )


def turma_path(instance, filename):
    return 'atividades/{prof}/{turma}/{name}'.format(
        prof=instance.professor.id,
        turma=instance.id,
        name=filename,
    )


def submissao_path(instance, filename):
    return 'codigos/{aluno}/{atividade}/{name}'.format(
        aluno=instance.aluno.id,
        atividade=instance.atividade.id,
        name=filename,
    )


def zip_path(instance):
    return 'arquivos/codigos/{name}.zip'.format(
        atividade=instance.id,
        name=instance.nome
    )


class Aluno(models.Model):

    Id = models.CharField(max_length=50, help_text="Id do Aluno")
    nome = models.CharField(max_length=50, help_text="Nome do Aluno")
    user = models.ForeignKey(
        User,
        help_text="Usuário de login relacionado ao Aluno",
    )

    def __str__(self):
        return '%s' % (self.nome.encode('utf-8'))

    def json_data(self):
        data = {}
        data['nome'] = self.nome
        data['username'] = self.user.get_username()
        data['email'] = self.user.email
        data['class'] = type(self).__name__
        return data


class Professor(models.Model):

    Id = models.CharField(max_length=50, help_text="Id do Professor")
    nome = models.CharField(max_length=50, help_text="Nome do Professor")
    user = models.ForeignKey(
        User,
        help_text="Usuário de login relacionado ao Professor",
    )

    def __str__(self):
        return '%s' % (self.nome.encode('utf-8'))

    def json_data(self):
        data = {}
        data['nome'] = self.nome
        data['username'] = self.user.get_username()
        data['email'] = self.user.email
        data['class'] = type(self).__name__
        return data


class Turma(models.Model):

    Id = models.CharField(max_length=50, help_text="Id da Turma")
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=2000)
    professor = models.ForeignKey(Professor, help_text="Professor da Turma")
    alunos = models.ManyToManyField(
        Aluno,
        help_text="Alunos inscritos na turma",
        blank=True,
    )

    def path(self, name):
        return turma_path(self, name)

    def __str__(self):
        return '%s %s' % (
            self.nome.encode('utf-8'),
            self.professor.nome.encode('utf-8')
        )


class Atividade(models.Model):

    def estaFechada(self):
        return self.data_limite < timezone.now().date()

    def path(self, name):
        return atividade_path(self, name)

    def countSubmissoes(self):
        counterSubmissoes = 0
        for relAlunoAtividade in RelAlunoAtividade.objects.filter(
                atividade=self):
            if relAlunoAtividade.foiEntregue:
                counterSubmissoes = counterSubmissoes + 1
        return counterSubmissoes

    def prof_json_data(self):
        data = {}
        data['id'] = self.Id
        data['nome'] = self.nome
        data['professor'] = self.turma.professor.nome
        data['prazo'] = self.data_limite
        data['submissoes'] = self.countSubmissoes()

        return data

    Id = models.CharField(max_length=50, help_text="Id da Submissao")
    nome = models.CharField(max_length=50)
    descricao = models.CharField(
        max_length=1000,
    )
    restricoes = models.CharField(
        max_length=1000,
    )
    arquivo_roteiro = models.FileField(upload_to=atividade_path)
    arquivo_entrada = models.FileField(upload_to=atividade_path)
    arquivo_saida = models.FileField(upload_to=atividade_path)
    data_limite = models.DateField()
    turma = models.ForeignKey(
        Turma,
        help_text="Turma a qual a atividade pertence",
    )
    alunos = models.ManyToManyField(
        Aluno,
        through='RelAlunoAtividade',
        help_text="""Relacao do aluno com a atividade,
            guarda se aluno submeteu atividade""",
        blank=True,
    )

    def __str__(self):
        return '%s %s' % (
            self.nome.encode('utf-8'), self.turma.nome.encode('utf-8'))

    def nome_roteiro(self):
        return os.path.basename(self.arquivo_roteiro.name)

    def nome_entrada(self):
        return os.path.basename(self.arquivo_entrada.name)

    def nome_saida(self):
        return os.path.basename(self.arquivo_saida.name)

    def zip_path(self):
        return zip_path(self)

    def remove_roteiro(self, *args, **kwargs):
        os.remove(
            os.path.join(
                settings.MEDIA_ROOT,
                self.arquivo_roteiro.name))

    def remove_entrada(self, *args, **kwargs):
        os.remove(
            os.path.join(
                settings.MEDIA_ROOT,
                self.arquivo_entrada.name))

    def remove_saida(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.arquivo_saida.name))


class Submissao(models.Model):

    RESULTADOS = (
        ('AC', 'Aceito'),
        ('TLE', 'Tempo Limite Excedido'),
        ('RTE', 'Erro em tempo de execução'),
        ('CE', 'Erro de compilação'),
        ('WA', 'Resposta Errada'),
    )
    data_envio = models.DateField(
        auto_now=True,
        help_text='Data de submissão do código',
    )
    arquivo_codigo = models.FileField(upload_to=submissao_path)
    resultado = models.CharField(
        max_length=3,
        choices=RESULTADOS,
        help_text='Resultado da submissao do aluno',
    )
    nota = models.PositiveSmallIntegerField(
        help_text='Nota para submissão do aluno'
    )
    atividade = models.ForeignKey(
        Atividade,
        help_text="Atividade relacionada a submissão"
    )
    aluno = models.ForeignKey(
        Aluno,
        help_text="Aluno que enviou a submissão")

    def nome_codigo(self):
        return os.path.basename(self.arquivo_codigo.name)

    def remove_file(self, *args, **kwargs):
        os.remove(
            os.path.join(
                settings.MEDIA_ROOT,
                self.arquivo_codigo.name))

    def __str__(self):
        return '%s %s' % (
            self.atividade.nome.encode('utf-8'),
            self.aluno.nome.encode('utf-8')
        )


class RelAlunoAtividade(models.Model):

    foiEntregue = models.BooleanField(
        help_text='Se o aluno já mandou alguma submissão para a atividade'
    )
    aluno = models.ForeignKey(Aluno, help_text="Aluno inscrito na atividade")
    atividade = models.ForeignKey(Atividade, help_text="Atividade do aluno")

    def aluno_json_data(self):
        data = {}
        data['entrega'] = self.foiEntregue
        data['id'] = self.atividade.Id
        data['nome'] = self.atividade.nome
        data['turma'] = self.atividade.turma.nome
        data['professor'] = self.atividade.turma.professor.nome
        data['prazo'] = self.atividade.data_limite

        return data

    def nota_json_data(self):
        data = {}
        if self.foiEntregue:
            submissao = Submissao.objects.filter(
                atividade=self.atividade, aluno=self.aluno
            ).first()
            data['nota'] = submissao.nota
            data['envio'] = submissao.data_envio
        return data

    def __str__(self):
        return '%s %s' % (
            self.atividade.nome.encode('utf-8'),
            self.aluno.nome.encode('utf-8')
        )
