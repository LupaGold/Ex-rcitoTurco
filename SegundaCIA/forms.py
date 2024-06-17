from django import forms 
from .models import Relatório2CIA, AvaliaçãoTP, Destaque2CIA
from django_ckeditor_5.widgets import CKEditor5Widget

class AvaliaçãoTPForm(forms.ModelForm):
    class Meta:
        model = AvaliaçãoTP
        fields = ['data', 'treinador_nick', 'tp']
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control'}),
            'treinador_nick': forms.TextInput(attrs={'class': 'form-control'}),
            'tp': forms.Select(attrs={'class': 'form-control'}),
        }

class Relatório2CIAForm(forms.ModelForm):
    hora_ino = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time','class': 'form-control'}), label='Hora de início')
    hora_fim = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time','class': 'form-control'}), label='Hora de término')
    
    class Meta:
        model = Relatório2CIA
        fields = ['hora_ino', 'hora_fim', 'treinador_patente', 'treinador_nick', 'avaliador_patente', 'avaliador', 'treinamento', 'ortografia', 'agilidade', 'aprofundamento', 'total', 'obs']
        widgets = {
            'treinador_patente': forms.Select(attrs={'class': 'form-control'}),
            'treinador_nick': forms.TextInput(attrs={'class': 'form-control'}),
            'avaliador_patente': forms.Select(attrs={'class': 'form-control'}),
            'avaliador': forms.Select(attrs={'class': 'form-control'}),
            'treinamento': forms.Select(attrs={'class': 'form-control'}),
            'ortografia': forms.NumberInput(attrs={'class': 'form-control'}),
            'agilidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'aprofundamento': forms.NumberInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
            'obs': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class Destaque2CIAForm(forms.ModelForm):
    class Meta:
        model = Destaque2CIA
        fields = ['militar']
        widgets = {
            'militar': forms.Select(attrs={'class': 'form-control'}),
        }