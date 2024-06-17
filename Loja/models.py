from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

#Class de emblemas da loja
class EmblemasModel(models.Model):
    #Militar responsável pela alteração na honraria
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitanteemblemas')
    #Título da pagina
    titulo = models.TextField(blank=False, null=True, max_length=30)
    #Valor do emblema
    moedas = models.FloatField(default=0.0)
    #Data do envio
    datatime = models.DateTimeField(default=timezone.now)
    #Icone da honraria
    icone = models.ImageField(upload_to='imagens/')

    def __str__(self):
        return self.titulo

class EmblemaCompra(models.Model):
    #Militar responsável pela alteração na honraria
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='comprador')
    #Emblema relacionado
    emblema = models.ForeignKey(EmblemasModel, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return f'{self.emblema} comprado por {self.solicitante}'

#Class de emblemas da loja
class MoedaValor(models.Model):
    #Militar responsável pela alteração na honraria
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantesaque')
    #Título da pagina
    titulo = models.TextField(blank=False, null=True, max_length=30)
    #Valor do emblema
    moedas = models.FloatField(default=0.0)
    #Data do envio
    datatime = models.DateTimeField(default=timezone.now)
    #Icone da honraria
    icone = models.ImageField(upload_to='imagens/')

    def __str__(self):
        return self.titulo

class MoedaSaqueMoedaValor(models.Model):
    #Data do envio
    datatime = models.DateTimeField(default=timezone.now)
    #Militar responsável pela alteração na honraria
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='militarsaque')
    #Emblema relacionado
    icone = models.ForeignKey(MoedaValor, on_delete=models.CASCADE,blank=True, null=True)

    status = models.TextField(blank=False, null=True, max_length=30)
    def __str__(self):
        return f'{self.icone} comprado por {self.solicitante}'