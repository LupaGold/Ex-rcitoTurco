from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth import get_user_model
from Avais.choices import PATENTES
from django.utils import timezone

#Model palestra
class PalestraSupervisores(models.Model):
    #Titulo da palestra
    titulo = models.TextField(blank=False, null=True, max_length=60)
    #Texto da palestra
    palestra =CKEditor5Field('palestrasup', config_name='extends', default=' ')

    def __str__(self):
        return self.titulo

class SupervisorRelatorio(models.Model):
    datatime = models.DateTimeField(default=timezone.now)
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True)
    palestra = models.ForeignKey(PalestraSupervisores, on_delete=models.CASCADE)
    patente_treinado = models.CharField(choices=PATENTES, blank=True, null=True, max_length=50)
    treinados = models.TextField(blank=True, null=True, max_length=50)
    treinador = models.TextField(blank=True, null=True, max_length=20)
    status = models.TextField(blank=False, max_length=50,null=True, default='Em análise...')

    def __str__(self):
        return f"{self.solicitante},{self.palestra}"
    
class GuiaSupervisores(models.Model):
    guia = CKEditor5Field('Guia', config_name='extends')
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantesup')
    datatime = models.DateTimeField(default=timezone.now)

class DestaqueSupervisor(models.Model):
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantedestsup')
    militar = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='militardestaquesup')
    datatime = models.DateTimeField(default=timezone.now)