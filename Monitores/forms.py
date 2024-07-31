from django import forms 
from .models import MonitorRelatorio, GuiaMonitores, DestaqueMonitores
from Avais.choices import STATUS, PATENTES, TREINAMENTOS
from django_ckeditor_5.widgets import CKEditor5Widget

class MonitorForm(forms.ModelForm):
    treinamento = forms.ChoiceField(choices=TREINAMENTOS,widget=forms.Select(attrs={'class': 'form-control'}),label='Treinamento:')
    treinados = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': '- Fulano', 'rows': 4}),label='Treinados:')
    patente_treinado = forms.ChoiceField(choices=PATENTES,widget=forms.Select(attrs={'class': 'form-control'}),label='Patente Treinados:')
    treinador_nick = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname'}),label='Treinador:')

    class Meta:
        model = MonitorRelatorio
        fields = ['treinamento', 'patente_treinado','treinados', 'treinador_nick']

class GuiaMonitoresForm(forms.ModelForm):
    class Meta:
        model = GuiaMonitores
        fields = ['guia',]
        widgets = {
            'guia': CKEditor5Widget(),
        }

class DestaqueMonitoresForm(forms.ModelForm):
    class Meta:
        model = DestaqueMonitores
        fields = ['militar']
        widgets = {
            'militar': forms.Select(attrs={'class': 'form-control'}),
        }