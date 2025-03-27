from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django_recaptcha.fields import ReCaptchaField
from django.contrib.auth.forms import PasswordChangeForm
from Militares.models import MilitarUsuario
from django.contrib.auth.forms import UserCreationForm
from Painel.models import DestaqueOficial, DestaquePraça

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nickname',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Digite seu nick'}))
    password = forms.CharField(label='Senha',widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Digite sua senha'}))
    # captcha = ReCaptchaField(label='')

class CadastroForm(forms.Form):
    username = forms.CharField(label='Nick:', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Digite seu nick'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Digite sua senha'}))
    confirm_password = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Confirme sua senha'}))
    codigo_aleatorio = forms.CharField(widget=forms.HiddenInput(),required=False)

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Senha antiga',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Nova senha',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirmar nova senha',widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class MilitarUsuarioCreationForm(forms.ModelForm):
    PATENTE_CHOICES = [
          ('', 'Selecione a Patente'),
            ('Soldado', 'Soldado'),
            ('Soldado de 1ª Classe', 'Soldado de 1ª Classe'),
            ('Especialista', 'Especialista'),
            ('Cabo', 'Cabo'),
            ('Aluno', 'Aluno'),
            ('Sargento', 'Sargento'),
            ('Sargento Staff', 'Sargento Staff'),
            ('Sargento Mestre', 'Sargento Mestre'),
            ('Sargento Major', 'Sargento Major'),
            ('Cadete', 'Cadete'),
            ('Aspirante-a-Oficial', 'Aspirante-a-Oficial'),
            ('Segundo Tenente', 'Segundo Tenente'),
            ('Primeiro Tenente', 'Primeiro Tenente'),
            ('Capitão', 'Capitão'),
            ('Major', 'Major'),
            ('Tenente-Coronel', 'Tenente-Coronel'),
            ('Coronel', 'Coronel'),
            ('Brigadeiro-General ★', 'Brigadeiro-General ★'),
            ('Major-General ★★', 'Major-General ★★'),
            ('Tenente-General ★★★', 'Tenente-General ★★★'),
            ('General-de-Exército ★★★★', 'General-de-Exército ★★★★'),
    ]

    patente = forms.ChoiceField(choices=PATENTE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = MilitarUsuario
        fields = ['username', 'patente', 'siglas']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'siglas': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nome de usuário'
        self.fields['patente'].label = 'Patente'
        self.fields['siglas'].label = 'Siglas'

class DestaquePraçaForm(forms.ModelForm):
    class Meta:
        model = DestaquePraça
        fields = ['militar']
        widgets = {
            'militar': forms.Select(attrs={'class': 'form-control'}),
        }

class DestaqueOficialForm(forms.ModelForm):
    class Meta:
        model = DestaqueOficial
        fields = ['militar']
        widgets = {
            'militar': forms.Select(attrs={'class': 'form-control'}),
        }