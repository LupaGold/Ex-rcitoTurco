from django.db import models
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField
from django.core.exceptions import ValidationError
from .choices import PATENTESALL, DURACAO, PATENTES, STATUS, TREINAMENTOSLIMITADOS, SALA, CATEGORIA, CONTADOR, TREINAMENTOS, PATRULHEIRO_ESCOLHA, CONTADORAPROVADOS
from django.contrib.auth import get_user_model
from Militares.models import MilitarUsuario
from django.utils.functional import lazy
from django_ckeditor_5.fields import CKEditor5Field

#Relatório de Treinamento Base (T1, T2, T3...)
class RelatoriosDeTreinamento(models.Model): 
    #Função que valida se o nick digitado corresponde a algum militar alistado relacionado.
    def Validador_Auxiliar(value):
        if not MilitarUsuario.objects.filter(username=value).exists():
            raise ValidationError(f"O nickname '{value}' não corresponde a nenhum militar alistado.")

    #Usuário que enviou o treinamento
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitante')
    #Data e hora do envio
    data = models.DateTimeField(default=timezone.now)
    #Oficial responsável
    ofc = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='oficial')
    #Treinador
    treinador = models.TextField(blank=True, null=True, max_length=50, validators=[Validador_Auxiliar])
    #Auxiliar
    auxiliar = models.TextField(blank=True, null=True, max_length=50, validators=[Validador_Auxiliar])
    #Treinamento
    treinamento = models.CharField(choices=TREINAMENTOSLIMITADOS, blank=False, null=True, max_length=50)
    #Sala de treinamento utilizada
    sala = models.CharField(choices=SALA, blank=False, null=True, max_length=50)
    #Treinados
    treinados = models.TextField(blank=True, null=True, max_length=50)
    #Hora de início
    hora_ino = models.TimeField(blank=False, null=True,)
    #Horário de finalização
    hora_fim = models.TimeField(blank=False, null=True,)
    #Contador de alistados
    alistado_cont = models.CharField(max_length=2,blank=False, null=True, choices=CONTADOR)
    #Contador de alistados
    reprovado_cont = models.CharField(max_length=2,blank=False, null=True, choices=CONTADORAPROVADOS)
    #Categoria do treinado (Recruta, Cabo...)
    categoria = models.CharField(choices=CATEGORIA, blank=False, null=True, max_length=50)
    #Reprovados
    reprovacoes = models.TextField(blank=False, null=True, max_length=250)
    #Aprovados
    aprovados = models.TextField(blank=False, null=True, max_length=250, default=' ')
    #Observações
    obs = models.CharField(blank=True, null=True, max_length=250)
    #Status do relatório de treinamento
    status = models.CharField(choices=STATUS,blank=False, max_length=50,null=True, default='Em análise...')
    #Oficial que aprovou/reprovou o relatório
    aprovador = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='aprovador')
    #Motivo da reprovação/justificativa de erros
    motivo = models.TextField(blank=True, null=True, max_length=250)

    def __str__(self):
        return f'{self.treinamento} enviado por {self.solicitante} em {self.data}.'
    

class LogRelatorio(models.Model):
      #Relatório de treinamento relacionado a log
      relatorio = models.ForeignKey(RelatoriosDeTreinamento, verbose_name=("relatorio"), on_delete=models.PROTECT, null=True)
      #Texto da log
      texto = models.TextField(blank=False, null=True, verbose_name='Texto relatorio', max_length=150)
      #Data e tempo de criação da log
      datatime = models.DateTimeField(default=timezone.now)

