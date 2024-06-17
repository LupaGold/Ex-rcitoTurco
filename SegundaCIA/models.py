from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field
from Militares.models import MilitarUsuario
from django.core.validators import MaxValueValidator, MinValueValidator

class Treinamentos(models.Model):
    #Usuário que registrou o treinamento
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantetreinamentos')
    #Título do treinamento
    titulo = models.TextField(blank=False, null=True, max_length=30)
    #Treinamento escrito no Editor de texto
    treinamento = CKEditor5Field('Treinamentos', config_name='extends', default=' ')
    #Data e tempo de atualização do treinamento
    datatime = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.titulo
    
class LogTreinamento(models.Model):
      #Treinamento relacionado a log
      treinamento = models.ForeignKey(Treinamentos, verbose_name=("treinamento"), on_delete=models.PROTECT, null=True)
      #Texto da log
      texto = models.TextField(blank=False, null=True, verbose_name='Texto relatorio', max_length=150)
      #Data e tempo de criação da log
      datatime = models.DateTimeField(default=timezone.now)

class Relatório2CIA(models.Model):
    PATENTES_AVAL = (
         ('', 'Selecione a patente'),
         ('Terceiro Sargento','Terceiro Sargento'),
         ('Segundo Sargento','Segundo Sargento'),
         ('Primeiro Sargento','Primeiro Sargento'),
         ('Subtenente','Subtenente'),
         ('Cadete','Cadete'),
    )
    PATENTES_AVALIADOR = (
         ('', 'Selecione a patente'),
         ('Segundo Tenente','Segundo Tenente'),
         ('Primeiro Tenente','Primeiro Tenente'),
         ('Capitão','Capitão'),
         ('Major','Major'),
         ('Tenente-Coronel','Tenente-Coronel'),
    )
    TREINAMENTOSLIMITADOS2CIA = (
        ('', 'Selecione o treinamento'),
        ('Básico I', 'Básico I'),
        ('Básico II', 'Básico II'),
        ('Complementar I', 'Complementar I'),
        ('Complementar II', 'Complementar II'),
        ('Robotizado I', 'Robotizado I'),
        ('Robotizado II', 'Robotizado II'),
    )
    
    data = models.DateTimeField(default=timezone.now)
    hora_ino = models.TimeField(blank=False, null=True,)
    hora_fim = models.TimeField(blank=False, null=True,)
    treinador_patente = models.CharField(choices=PATENTES_AVAL, blank=False, null=True, max_length=50)
    treinador_nick = models.TextField(blank=True, null=True, max_length=20)
    avaliador_patente = models.CharField(choices=PATENTES_AVALIADOR, blank=False, null=True, max_length=50) 
    avaliador = models.ForeignKey(MilitarUsuario, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'M2CIA'})
    treinamento = models.CharField(choices=TREINAMENTOSLIMITADOS2CIA, blank=False, null=True, max_length=50) 
    ortografia = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, help_text='Digite um valor entre 0,0 e 4,0')
    agilidade = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], help_text='Digite um valor entre 0,0 e 1,0')
    aprofundamento = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], help_text='Digite um valor entre 0,0 e 5,0')
    total = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, help_text='Digite um valor entre 0,0 e 10,0')
    obs = models.TextField(blank=True, null=True, max_length=250)

class AvaliaçãoTP(models.Model):
    TIPO_TP = (
          ('', 'Selecione o tipo de TP'),
          ('Tp1', 'Tp1'),
          ('Tp2', 'Tp2'),
          ('Tp3', 'Tp3'),
          ('Tp4', 'Tp4'),
     )

    data = models.DateTimeField(default=timezone.now)
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True)
    treinador_nick = models.TextField(blank=True, null=True, max_length=20)
    tp = models.CharField(choices=TIPO_TP, blank=False, null=True, max_length=50)

class Destaque2CIA(models.Model):
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantedest2cia')
    militar = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='militardestaque2cia')
    datatime = models.DateTimeField(default=timezone.now)