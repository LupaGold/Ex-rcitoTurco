from django import forms
from .models import EmblemasModel

class EmblemasForm(forms.ModelForm):
    class Meta:
        model = EmblemasModel
        fields = [ 'titulo', 'moedas', 'icone']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'moedas': forms.NumberInput(attrs={'class': 'form-control'}),
        }