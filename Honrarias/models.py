from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.text import slugify

#Class das honrarias
class HonrariasRegistro(models.Model):
    #Militar responsável pela alteração na honraria
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantehonraria')
    #Título da pagina
    titulo = models.TextField(blank=False, null=True, max_length=30)
    #Descrição da pagina
    descricao = models.TextField(blank=False, null=True, max_length=400)
    #Data e tempo da honraria
    datatime = models.DateTimeField(default=timezone.now)
    #Icone da honraria
    icone = models.ImageField(upload_to='imagens/')
    #Imagem medalha da honraria
    imagem = models.ImageField(upload_to='imagens/')

    def __str__(self):
        return self.titulo
    

#Classe relaciona honraria ao militar
class HonrariaMilitar(models.Model):
    #Militar responsável pela alteração na honraria
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantehonrariamilitar')
    #Militar honrado
    militar = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='militarhonraria')
    #Honraria selecionada
    honraria = models.ForeignKey(HonrariasRegistro, on_delete=models.CASCADE,blank=True, null=True, related_name='honraria' )
    #Data e tempo da honraria
    datatime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.militar.patente} {self.militar.username} - {self.honraria.titulo}'
