from django import forms
from .models import RelatoriosDeTreinamento
from Militares.models import MilitarUsuario
from .choices import STATUS, SALA, DURACAO, PATENTES, TREINAMENTOSLIMITADOS, CONTADOR, CONTADORAPROVADOS, CATEGORIA, TREINAMENTOS, PATRULHEIRO_ESCOLHA

#Formulário de envio de relatórios de treinamentos
class RelatorioDeTreinamentoForm(forms.ModelForm):
    #Campos
    data = forms.DateField(required=False,widget=forms.HiddenInput())
    hora_ino = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    hora_fim = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    treinador = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname'}))
    auxiliar = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname'}))
    treinamento = forms.ChoiceField(choices=TREINAMENTOSLIMITADOS,widget=forms.Select(attrs={'class': 'form-control'}))
    categoria = forms.ChoiceField(choices=CATEGORIA,widget=forms.Select(attrs={'class': 'form-control'}))
    sala = forms.ChoiceField(choices=SALA,widget=forms.Select(attrs={'class': 'form-control'}))
    treinados = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': '- Fulano', 'rows': 4}))
    alistado_cont = forms.ChoiceField(choices=CONTADOR,widget=forms.Select(attrs={'class': 'form-control'}))
    reprovado_cont = forms.ChoiceField(choices=CONTADORAPROVADOS,widget=forms.Select(attrs={'class': 'form-control'}))
    reprovacoes = forms.CharField(required=False,widget=forms.Textarea(attrs={'class': 'form-control','placeholder': '- Às [22:33], o Patente Fulano, foi reprovado. Motivo: Saiu durante o treinamento.', 'rows': 4}))
    obs = forms.CharField(required=False,widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'- Como foi o treinamento? - Atitudes do treinador. - Como é a forma que o treinador escreve? - Aconteceu algo anormal?', 'rows': 4 }))
    aprovados = forms.CharField(required=False,widget=forms.Textarea(attrs={'class': 'form-control','placeholder': '- Fulano', 'rows': 4}))

    #Meta dos campos
    class Meta:
        model = RelatoriosDeTreinamento
        fields = ['aprovados', 'ofc',  'treinador', 'auxiliar', 'treinamento', 'sala', 'treinados', 'hora_ino', 'hora_fim', 'alistado_cont', 'reprovado_cont', 'reprovacoes', 'obs', 'categoria']

    #Filtro de oficiais para o campo de responsáveis
    def __init__(self, *args, **kwargs):
        super(RelatorioDeTreinamentoForm, self).__init__(*args, **kwargs)
        PATENTE_CHOICES = [
            'Aspirante-a-Oficial', 'Segundo Tenente', 'Primeiro Tenente', 'Capitão', 
            'Major', 'Tenente-Coronel', 'Coronel ★', 'General-de-Brigada ★★', 
            'General-de-Divisão ★★★', 'General-de-Exército ★★★★', 'Marechal ★★★★★'
        ]
        self.fields['ofc'].queryset = MilitarUsuario.objects.filter(patente__in=PATENTE_CHOICES, status='Ativo').order_by('patente_order')
        self.fields['ofc'].widget.attrs.update({'class': 'form-control'})
        self.fields['ofc'].label_from_instance = lambda obj: f'{obj.patente} - {obj.username}'