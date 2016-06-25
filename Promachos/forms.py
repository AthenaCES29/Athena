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
            'nome', 'descricao', 'data_limite', 'arquivo_roteiro'
        ]
        labels = {
            'nome': u'Nome da atividade*',
            'descricao': u'Descricao da atividade*',
            'data_limite': u'Data limite de entrega*',
            'arquivo_roteiro': u'Arquivo com roteiro',
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Ex.: Lab 1-Printf',
                'required': 'True',
            }),
            'data_limite': forms.TextInput(attrs={
                'class': 'date_picker',
                'required': 'True',
            }),
            'descricao': forms.Textarea(attrs={
                'placeholder': 'Ex.: Lab que ensina a fazer printf',
                'required': 'False',
                'rows': '5',
            }),
            'arquivo_roteiro': forms.FileInput(attrs={
                'required': 'True',
            })
        }


class AtividadeEditForm(ModelForm):

    class Meta:
        model = Atividade
        fields = [
            'nome', 'descricao', 'data_limite', 'arquivo_roteiro'
        ]
        labels = {
            'nome': u'Nome da atividade',
            'descricao': u'Descricao da atividade',
            'data_limite': u'Data limite de entrega',
            'arquivo_roteiro': u'Novo arquivo com o roteiro (opcional)',
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Ex.: Lab 1-Printf',
            }),
            'descricao': forms.Textarea(attrs={
                'placeholder': 'Ex.: Lab que ensina a fazer printf',
                'rows': '5',
            }),
            'data_limite': forms.DateInput(attrs={
                'class': 'date_picker',
            }),
            'arquivo_roteiro': forms.FileInput(attrs={
            })
        }
