from django import forms 
from .models import AjudanteRelatorio, GuiaAjudantes, DestaqueAjudantes
from Avais.choices import STATUS, PATENTES
from django_ckeditor_5.widgets import CKEditor5Widget

OP = (
          ('Mover (TS) (1)','Mover (TS) (1)'),
          ('Mudança de Patente (TS) (1)','Mudança de Patente (TS) (1)'),
          ('Instalação do TeamSpeak (4)','Instalação do TeamSpeak (4)'),
          ('Instalação de Discord (2)','Instalação de Discord (2)'),
          ('Instalação do Lightshot (2)','Instalação do Lightshot (2)'),
          ('Instalação do Launcher (2)','Instalação do Launcher (2)'),
          ('Cidadania Habbo (3)','Cidadania Habbo (3)'),
          ('Configuração do TeamSpeak (2)','Configuração do TeamSpeak (2)'),
          ('Auxilio com WhatsApp (3)','Auxilio com WhatsApp (3)'),
          ('Ajudar a entrar no QG (1)','Ajudar a entrar no QG (1)'),
)

class GuiaAjudanteForm(forms.ModelForm):
    class Meta:
        model = GuiaAjudantes
        fields = ['guia',]
        widgets = {
            'guia': CKEditor5Widget(),
        }

class AjudanteForm(forms.ModelForm):
    palestra = forms.ChoiceField(choices=OP, widget=forms.Select(attrs={'class': 'form-control'}))
    treinados = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': '- Fulano', 'rows': 4}),label='Treinados:')
    patente_treinado = forms.ChoiceField(choices=PATENTES,widget=forms.Select(attrs={'class': 'form-control'}),label='Patente Treinados:')
    treinador = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname'}),label='Treinador:')

    class Meta:
        model = AjudanteRelatorio
        fields = ['palestra','treinador', 'patente_treinado','treinados']

class DestaqueAjudanteForm(forms.ModelForm):
    class Meta:
        model = DestaqueAjudantes
        fields = ['militar']
        widgets = {
            'militar': forms.Select(attrs={'class': 'form-control'}),
        }