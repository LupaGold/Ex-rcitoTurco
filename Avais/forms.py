from django import forms
from .models import JA
from .choices import DURACAO

#Formulário de envio de JA's
class JAForm(forms.ModelForm):
    #Campos
    motivo = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Digite o motivo do afastamento aqui.'}), label='Motivo:', max_length=150)
    duracao = forms.ChoiceField(choices=DURACAO, widget=forms.Select(attrs={'class': 'form-control'}), label='Duração:')
    data = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label='Data de Ida:')
    data2 = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label='Data de Volta:')

    #Meta dos campos
    class Meta:
        model = JA
        fields = ['motivo','duracao', 'data', 'data2']