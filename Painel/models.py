from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from Militares.models import MilitarUsuario
from django_ckeditor_5.fields import CKEditor5Field

class DestaqueOficial(models.Model):
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantedest3oficial')
    militar = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='militardestaqueoficial')
    datatime = models.DateTimeField(default=timezone.now)

class DestaquePraça(models.Model):
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantedest3praça')
    militar = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='militardestaquepraça')
    datatime = models.DateTimeField(default=timezone.now)

class Aviso(models.Model):
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='aviso')
    aviso = models.TextField(blank=True, null=True, max_length=250)    
    datatime = models.DateTimeField(default=timezone.now)

class Documentos(models.Model):
    categoria = models.TextField(blank=True, null=True, max_length=250) 
    guia = CKEditor5Field('Documentos', config_name='extends')
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='documentos')
    datatime = models.DateTimeField(default=timezone.now)