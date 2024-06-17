from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from Militares.models import MilitarUsuario

class Relatório3CIA(models.Model):
    EVENTO = (
        ('', 'Selecione o tipo de evento'),
        ('Evento rápido', 'Evento rápido'),
        ('Evento interno', 'Evento interno'),
        ('Evento externo', 'Evento externo'),
    )
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitanterelt3cia')
    data = models.DateTimeField(default=timezone.now)
    resp = models.ForeignKey(MilitarUsuario, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'M3CIA'})
    tipoevento = models.CharField(choices=EVENTO,blank=True, null=True, max_length=250)
    vencedores = models.TextField(blank=True, null=True, max_length=250)
    doacao = models.TextField(blank=True, null=True, max_length=250)
    obs = models.TextField(blank=True, null=True, max_length=250)

class Doação3CIA(models.Model):
    PAGAMENTO = (
        ('', 'Selecione o tipo de pagamento'),
        ('Moeda', 'Moeda'),
        ('Mobi', 'Mobi'),
    )

    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True)
    data = models.DateTimeField(default=timezone.now)
    valor = models.TextField(blank=True, null=True, max_length=250)
    doador = models.TextField(blank=True, null=True, max_length=250)
    pagamento = models.CharField(choices=PAGAMENTO, blank=False, null=True, max_length=50) 
    
class Destaque3CIA(models.Model):
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantedest3cia')
    militar = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='militardestaque3cia')
    datatime = models.DateTimeField(default=timezone.now)