from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from Avais.choices import STATUS

#Classe de RE
class Re(models.Model):
      #Data e tempo de abertura e fechamento
      abertura = models.DateTimeField(default=timezone.now)
      fechamento = models.DateTimeField(default=timezone.now)
      #Militar que enviou o JA
      solicitante = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,blank=True, null=True)
      #Oficial responsável
      ofc = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='oficialre')
      #Aprovados
      recrutados = models.TextField(blank=False, null=True, max_length=250, default=' ')
      #Status do JA
      status = models.CharField(choices=STATUS, blank=False, null=True, max_length=50, default='Em análise...')

#Log do RE
class LogRE(models.Model):
      #Aval relacionado a log
      re = models.ForeignKey(Re, verbose_name=("aval"), on_delete=models.PROTECT)
      #Texto da log
      texto = models.TextField(blank=False, null=True, verbose_name='Texto RE', max_length=150)
      #Data e tempo de criação da log
      datatime = models.DateTimeField(default=timezone.now)
