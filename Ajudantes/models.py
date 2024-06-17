from django.db import models
from django.contrib.auth import get_user_model
from Avais.choices import STATUS, PATENTES
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class AjudanteRelatorio(models.Model):
    OP = (
          ('Mover (TS) (1)','Mover (TS) (1)'),
          ('Mudança de Patente (TS) (1)','Mudança de Patente (TS) (1)'),
          ('Instalação do TeamSpeak (4)','Instalação do TeamSpeak (4)'),
          ('Instalação de Discord (2)','Instalação de Discord (2)'),
          ('Instalação do Lightshot (2)','Instalação do Lightshot (2)'),
          ('Instalação do Launcher (2)','Instalação do Launcher (2)'),
          ('Cidadania Habbo (3)','Cidadania Habbo (3)'),
          ('Configuração do TeamSpeak (2)','Configuração do TeamSpeak (2)'),
          ('Auxilio com WhatsApp (3)','Auxilio com WhatsApp (3)'),
          ('Ajudar a entrar no QG (1)','Ajudar a entrar no QG (1)'),
)
    data = models.DateTimeField(default=timezone.now)
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True)
    palestra = models.CharField(OP, blank=True, null=True, max_length=50)
    patente_treinado = models.CharField(choices=PATENTES, blank=True, null=True, max_length=50)
    treinados = models.TextField(blank=True, null=True, max_length=50, default='')
    treinador = models.TextField(blank=True, null=True, max_length=20)

    def __str__(self):
        return f"{self.solicitante},{self.palestra}"
    
class GuiaAjudantes(models.Model):
    guia = CKEditor5Field('Guia', config_name='extends')
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitanteajd')
    datatime = models.DateTimeField(default=timezone.now)

class DestaqueAjudantes(models.Model):
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantedestajd')
    militar = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='militardestaqueajd')
    datatime = models.DateTimeField(default=timezone.now)