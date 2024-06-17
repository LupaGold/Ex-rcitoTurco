from django import forms 
from .models import Re
from Militares.models import MilitarUsuario

#Classe dos forms
class ReForm(forms.ModelForm):
    #Classe meta dos campos
    class Meta:
        model = Re
        fields = ['ofc']

    #Filtro de oficiais para o campo de responsáveis
    def __init__(self, *args, **kwargs):
        super(ReForm, self).__init__(*args, **kwargs)
        PATENTE_CHOICES = [
            'Aspirante-a-Oficial', 'Segundo Tenente', 'Primeiro Tenente', 'Capitão', 
            'Major', 'Tenente-Coronel', 'Coronel ★', 'General-de-Brigada ★★', 
            'General-de-Divisão ★★★', 'General-de-Exército ★★★★', 'Marechal ★★★★★'
        ]
        self.fields['ofc'].queryset = MilitarUsuario.objects.filter(patente__in=PATENTE_CHOICES, status='Ativo').order_by('patente_order')
        self.fields['ofc'].widget.attrs.update({'class': 'form-control'})
        self.fields['ofc'].label_from_instance = lambda obj: f'{obj.patente} - {obj.username}'

