# -*- coding: utf-8 -*-
import os,sys
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from Athena import settings


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
    return 'codigos/{0}/{1}/{2}'.format(
        instance.aluno.id,
        instance.atividade.id,
        filename,
    )


class Aluno(models.Model):

    nome = models.CharField(max_length=50, help_text="Nome do Aluno")
    user = models.ForeignKey(
        User,
        help_text="Usuário de login relacionado ao Aluno",
    )

    def __str__(self):
        return '%s' % (self.nome.encode('utf-8'))


class Professor(models.Model):

    nome = models.CharField(max_length=50, help_text="Nome do Professor")
    user = models.ForeignKey(
        User,
        help_text="Usuário de login relacionado ao Professor",
    )

    def __str__(self):
        return '%s' % (self.nome.encode('utf-8'))


class Turma(models.Model):

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
        return '%s %s' % (self.nome.encode('utf-8'), self.professor.nome.encode('utf-8'))


class Atividade(models.Model):

    def estaFechada(self):
        return self.data_limite < timezone.now().date()

    def path(self, name):
        return atividade_path(self, name)

    nome = models.CharField(max_length=50)
    descricao = models.CharField(
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
        return '%s %s' % (self.nome.encode('utf-8'), self.turma.nome.encode('utf-8'))

    def nome_roteiro(self):
        return os.path.basename(self.arquivo_roteiro.name)

    def nome_entrada(self):
        return os.path.basename(self.arquivo_entrada.name)

    def nome_saida(self):
        return os.path.basename(self.arquivo_saida.name)

    def remove_roteiro(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.arquivo_roteiro.name))

    def remove_entrada(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.arquivo_entrada.name))

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
    aluno = models.ForeignKey(Aluno, help_text="Aluno que enviou a submissão")

    def nome_codigo(self):
        return os.path.basename(self.arquivo_codigo.name)

    def remove_file(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.arquivo_codigo.name))

    def __str__(self):
        return '%s %s' % (self.atividade.nome.encode('utf-8'), self.aluno.nome.encode('utf-8'))


class RelAlunoAtividade(models.Model):

    foiEntregue = models.BooleanField(
        help_text='Se o aluno já mandou alguma submissão para a atividade'
    )
    aluno = models.ForeignKey(Aluno, help_text="Aluno inscrito na atividade")
    atividade = models.ForeignKey(Atividade, help_text="Atividade do aluno")

    def __str__(self):
        return '%s %s' % (self.atividade.nome.encode('utf-8'), self.aluno.nome.encode('utf-8'))
