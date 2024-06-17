from django.db import models
import datetime
from .choices import DURACAO, PATENTES, STATUS, TREINAMENTOSLIMITADOS, SALA, CATEGORIA, CONTADOR, TREINAMENTOS, PATRULHEIRO_ESCOLHA, CONTADORAPROVADOS
from django.contrib.auth import get_user_model
from django.utils import timezone

#Aval para afastamento não remunerado
class JA(models.Model):
      #Data e tempo de criação
      datatime = models.DateTimeField(default=timezone.now)
      #Militar que enviou o JA
      solicitante = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,blank=True, null=True)
      #Duração do Aval
      duracao = models.CharField(choices=DURACAO, blank=False, null=True, max_length=50 )
      #Motivo do Aval
      motivo = models.TextField(blank=False, null=True, verbose_name='Motivo', max_length=150)
      #Data de início e de fim
      data = models.DateField(blank=False, null=True, default=datetime.date.today)
      data2 = models.DateField(blank=False, null=True, default=datetime.date.today)
      #Status do JA
      status = models.CharField(choices=STATUS, blank=False, null=True, max_length=50, default='Em análise...')
      
      def __str__(self):
        return f'Aval solicitado por {self.solicitante.patente} {self.solicitante.username} com duração de {self.duracao}, com início em {self.data} e termino em {self.data2}; Atual status: {self.status}.'

class LogJA(models.Model):
      #Aval relacionado a log
      aval = models.ForeignKey(JA, verbose_name=("aval"), on_delete=models.PROTECT)
      #Texto da log
      texto = models.TextField(blank=False, null=True, verbose_name='Texto Aval', max_length=150)
      #Data e tempo de criação da log
      datatime = models.DateTimeField(default=timezone.now)