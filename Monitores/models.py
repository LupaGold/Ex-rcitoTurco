from django.db import models
from django.contrib.auth import get_user_model
from Avais.choices import STATUS, PATENTES, TREINAMENTOS
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

class MonitorRelatorio(models.Model):
    data = models.DateTimeField(default=timezone.now)
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True)
    treinamento = models.CharField(choices=TREINAMENTOS, blank=False, null=True, max_length=50)
    patente_treinado = models.CharField(choices=PATENTES, blank=True, null=True, max_length=50)
    treinados = models.TextField(blank=True, null=True, max_length=50)
    treinador_nick = models.TextField(blank=True, null=True, max_length=20)
    status = models.CharField(choices=STATUS,blank=False, max_length=50,null=True, default='Em análise...')


    def __str__(self):
        return f"{self.solicitante},{self.treinamento}"
    
class GuiaMonitores(models.Model):
    guia = CKEditor5Field('Guia', config_name='extends')
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantemon')
    datatime = models.DateTimeField(default=timezone.now)

class DestaqueMonitores(models.Model):
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantedestmon')
    militar = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='militardestaquemon')
    datatime = models.DateTimeField(default=timezone.now)