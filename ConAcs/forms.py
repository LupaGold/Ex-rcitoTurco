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
    captcha = ReCaptchaField(label='')

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Senha antiga',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Nova senha',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirmar nova senha',widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class MilitarUsuarioCreationForm(forms.ModelForm):
    PATENTE_CHOICES = [
        ('Soldado', 'Soldado'),
        ('Cabo', 'Cabo'),
        ('Aluno', 'Aluno'),
        ('Terceiro Sargento', 'Terceiro Sargento'),
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