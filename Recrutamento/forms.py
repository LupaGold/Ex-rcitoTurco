from django import forms 
from .models import Re, RM
from Militares.models import MilitarUsuario

#Classe dos forms
class ReForm(forms.ModelForm):
    #Classe meta dos campos
    class Meta:
        model = Re
        fields = ['ofc','abertura','fechamento','militar','recrutados']

    #Filtro de oficiais para o campo de responsáveis
    def __init__(self, *args, **kwargs):
        super(ReForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        PATENTE_CHOICES = [
            'Aspirante-a-Oficial', 'Segundo Tenente', 'Primeiro Tenente', 'Capitão', 
            'Major', 'Tenente-Coronel', 'Coronel ★', 'General-de-Brigada ★★', 
            'General-de-Divisão ★★★', 'General-de-Exército ★★★★', 'Marechal ★★★★★'
        ]
        self.fields['ofc'].queryset = MilitarUsuario.objects.filter(patente__in=PATENTE_CHOICES, status='Ativo').order_by('patente_order')
        self.fields['ofc'].widget.attrs.update({'class': 'form-control','label':'Oficial'})
        self.fields['ofc'].label_from_instance = lambda obj: f'{obj.patente} - {obj.username}'

class RMForm(forms.ModelForm):
    link = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'https://imgur.com/'}),label='Link:')
    presentes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Major João, Major Pedro, Capitão Daniel e 2° Tenente Natan.', 'rows': 4}))
    #Classe meta dos campos
    class Meta:
        model = RM
        fields = ['ofc','hora','link','presentes']

    #Filtro de oficiais para o campo de responsáveis
    def __init__(self, *args, **kwargs):
        super(RMForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        PATENTE_CHOICES = [
            'Aspirante-a-Oficial', 'Segundo Tenente', 'Primeiro Tenente', 'Capitão', 
            'Major', 'Tenente-Coronel', 'Coronel ★', 'General-de-Brigada ★★', 
            'General-de-Divisão ★★★', 'General-de-Exército ★★★★', 'Marechal ★★★★★'
        ]
        self.fields['ofc'].queryset = MilitarUsuario.objects.filter(patente__in=PATENTE_CHOICES, status='Ativo').order_by('patente_order')
        self.fields['ofc'].widget.attrs.update({'class': 'form-control'})
        self.fields['ofc'].label_from_instance = lambda obj: f'{obj.patente} - {obj.username}'

