from django import forms
from .models import Comentario, Post

#Form do comentario
class ComentarioForm(forms.ModelForm):
    texto = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Digite aqui...'}), label='', max_length=150)

    class Meta:
        model = Comentario
        fields = ['texto']

#Form do post
class PostForm(forms.ModelForm):
    texto = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Digite aqui...'}), label='', max_length=150)

    class Meta:
        model = Post
        fields = ['texto']