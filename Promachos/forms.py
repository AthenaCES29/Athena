# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from Athena.models import Turma, Atividade


class UploadFileForm(forms.Form):

    file = forms.FileField()


class TurmaCreationForm(ModelForm):

    class Meta:
        model = Turma
        fields = ['nome', 'descricao']
        labels = {
            'nome': u'Nome da turma',
            'descricao': u'Descrição',
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Ex.: CES-10',
                'required': 'True',
                'class': 'form-group',
            }),
            'descricao': forms.Textarea(attrs={
                'placeholder': 'Ex.: Turma de CES-10 ministrada por João',
                'required': 'False',
                'rows': '5',
                'class': 'form-group',
            }),
        }


class AtividadeCreationForm(ModelForm):

    class Meta:
        model = Atividade
        fields = [
            'nome', 'descricao', 'arquivo_roteiro', 'arquivo_entrada', 'arquivo_entrada2',
            'arquivo_saida', 'arquivo_saida2', 'peso1', 'peso2', 'data_limite'
        ]
        labels = {
            'nome': u'Nome da atividade',
            'descricao': u'Descricao da atividade',
            'arquivo_roteiro': u'Arquivo com roteiro',
            'arquivo_entrada': u'Arquivo de entrada',
            'arquivo_entrada2': u'Arquivo de entrada privado',
            'arquivo_saida': u'Arquivo de saida',
            'arquivo_saida2': u'Arquivo de saida privado',
            'peso1': u'Peso do arquivo publico',
            'peso2': u'Peso do arquivo privado',
            'data_limite': u'Data limite de entrega',
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Ex.: Lab 1-Printf',
                'required': 'True',
            }),
            'descricao': forms.Textarea(attrs={
                'placeholder': 'Ex.: Lab que ensina a fazer printf',
                'required': 'False',
                'rows': '5',
            }),
            'arquivo_roteiro': forms.FileInput(attrs={
                'required': 'True',
            }),
            'arquivo_entrada': forms.FileInput(attrs={
                'required': 'True',
            }),
            'arquivo_entrada2': forms.FileInput(attrs={
                'required': 'True',
            }),
            'arquivo_saida': forms.FileInput(attrs={
                'required': 'True',
            }),
             'arquivo_saida2': forms.FileInput(attrs={
                'required': 'True',
            }),
            'peso1': forms.TextInput(attrs={
                'required': 'True',
            }),
            'peso2': forms.TextInput(attrs={
                'required': 'True',
            }),
            'data_limite': forms.TextInput(attrs={
                'class': 'date_picker',
                'required': 'True',
            }),

        }


class AtividadeEditForm(ModelForm):

    class Meta:
        model = Atividade
        fields = [
            'nome', 'descricao', 'arquivo_roteiro', 'arquivo_entrada','arquivo_entrada2',
            'arquivo_saida', 'arquivo_saida2', 'data_limite'
        ]
        labels = {
            'nome': u'Nome da atividade',
            'descricao': u'Descricao da atividade',
            'arquivo_roteiro': u'Arquivo com roteiro',
            'arquivo_entrada': u'Arquivo de entrada',
            'arquivo_entrada2': u'Arquivo de entrada privada',
            'arquivo_saida': u'Arquivo de saida',
            'arquivo_saida2': u'Arquivo de saida privada',
            'peso1': u'Peso do arquivo publico',
            'peso2': u'Peso do arquivo privado',
            'data_limite': u'Data limite de entrega',
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Ex.: Lab 1-Printf',
            }),
            'descricao': forms.Textarea(attrs={
                'placeholder': 'Ex.: Lab que ensina a fazer printf',
                'rows': '5',
            }),
            'arquivo_roteiro': forms.FileInput(attrs={
            }),
            'arquivo_entrada': forms.FileInput(attrs={
            }),
            'arquivo_entrada2': forms.FileInput(attrs={
            }),
            'arquivo_saida': forms.FileInput(attrs={
            }),
            'arquivo_saida2': forms.FileInput(attrs={
            }),
            'peso1': forms.TextInput(attrs={
            }),
            'peso2': forms.TextInput(attrs={
            }),
            'data_limite': forms.DateInput(attrs={
                'class': 'date_picker',
            }),
        }
