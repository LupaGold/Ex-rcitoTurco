from django import forms 
from .models import Relatório3CIA, Doação3CIA, Destaque3CIA

EVENTO = (
        ('', 'Selecione o tipo de evento'),
        ('Evento rápido', 'Evento rápido'),
        ('Evento interno', 'Evento interno'),
        ('Evento externo', 'Evento externo'),
    )

class Relatório3CIAForm(forms.ModelForm):
    tipoevento = forms.ChoiceField(choices=EVENTO, label='Tipo de Evento:', widget=forms.Select(attrs={'class': 'form-control'}))
    vencedores = forms.CharField(label='Vencedores:', widget=forms.Textarea(attrs={'placeholder': '- Fulano','class': 'form-control', 'rows': 4}))
    doacao = forms.CharField(required=False,label='Doação:', widget=forms.Textarea(attrs={'placeholder': '- Fulano','class': 'form-control', 'rows': 4}))
    obs = forms.CharField(required=False,label='Observações:', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    
    class Meta:
        model = Relatório3CIA
        fields = ['resp', 'tipoevento', 'vencedores', 'doacao', 'obs']
        widgets = {
            'resp': forms.Select(attrs={'class': 'form-control'}),
        }

class Doação3CIAForm(forms.ModelForm):
    class Meta:
        model = Doação3CIA
        fields = ['valor', 'doador', 'pagamento']
        widgets = {
            'valor': forms.TextInput(attrs={'class': 'form-control'}),
            'doador': forms.TextInput(attrs={'class': 'form-control'}),
            'pagamento': forms.Select(attrs={'class': 'form-control'}),
        }

class Destaque3CIAForm(forms.ModelForm):
    class Meta:
        model = Destaque3CIA
        fields = ['militar']
        widgets = {
            'militar': forms.Select(attrs={'class': 'form-control'}),
        }