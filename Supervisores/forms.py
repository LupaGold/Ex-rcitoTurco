from django import forms 
from .models import GuiaSupervisores, PalestraSupervisores, SupervisorRelatorio, DestaqueSupervisor
from django_ckeditor_5.widgets import CKEditor5Widget
from Avais.choices import PATENTES

class GuiaSupervisoresForm(forms.ModelForm):
    class Meta:
        model = GuiaSupervisores
        fields = ['guia',]
        widgets = {
            'guia': CKEditor5Widget(),
        }

class SupervisorForm(forms.ModelForm):
    palestra = forms.ModelChoiceField(queryset=PalestraSupervisores.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    treinados = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': '- Fulano', 'rows': 4}),label='Treinados:')
    patente_treinado = forms.ChoiceField(choices=PATENTES,widget=forms.Select(attrs={'class': 'form-control'}),label='Patente Treinados:')
    treinador = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname'}),label='Treinador:')

    class Meta:
        model = SupervisorRelatorio
        fields = ['palestra','treinador', 'patente_treinado','treinados']

class DestaqueSupervisorForm(forms.ModelForm):
    class Meta:
        model = DestaqueSupervisor
        fields = ['militar']
        widgets = {
            'militar': forms.Select(attrs={'class': 'form-control'}),
        }

class PalestraSupervisoresForm(forms.ModelForm):
    class Meta:
        model = PalestraSupervisores
        fields = ['titulo', 'palestra']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'palestra': CKEditor5Widget(),
        }