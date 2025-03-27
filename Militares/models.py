import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from .choices import PATENTES, STATUS, SIGLAS, MOTIVO
from django.utils.text import slugify


#Manager do MilitarUsuario
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('O nome de usuário é obrigatório')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

#Model Militar
class MilitarUsuario(AbstractUser):
    #Alteração no validador para incluir caracteres inválidos
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9@_:.,\-!=]+$',
            message=_('Enter a valid username. This value may contain only letters (uppercase and lowercase), numbers, @, :, -, and _ characters.'),
            code='invalid_username',
        )],
        help_text=_('150 characters or fewer. Letters (uppercase and lowercase), digits, @, :, -, and _ only.'),
    )
    #Patente do Militar
    patente = models.CharField(choices=PATENTES, blank=False, null=False, max_length=50, default='Soldado')
    #Siglas de treinamento
    siglas = models.CharField(choices=SIGLAS, blank=True, null=False, max_length=50)
    #Status (Ativo, Demitido, Exilado, Aposentado)
    status = models.CharField(choices=STATUS, blank=False, null=False, max_length=50, default='Ativo')
    #Motivo da demissão
    demissao_motivo = models.CharField(choices=MOTIVO, blank=True, null=False, max_length=50)
    #Responsável pela última promoção
    responsavel_promocao = models.TextField(blank=False, null=False, verbose_name='Responsável', max_length=50)
    #Data da última promoção
    data = models.DateField(default=datetime.date.today)
    #Moedas na carteira
    moedas = models.FloatField(default=0.0)
    #Log de IP
    ultimo_acesso = models.DateTimeField(null=True, blank=True)
    #Definindo o manage
    objects = CustomUserManager()
    #Ordem de patentes
    patente_order = models.IntegerField(default=0, editable=False)
    # Slug para URL amigável
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        patente_order_map = {
            'Marechal ★★★★★': 1,
            'General ★★★★': 2,
            'Tenente-General ★★★': 3,
            'Major-General ★★': 4,
            'Brigadeiro-General ★': 5,
            'Coronel': 6,
            'Tenente-Coronel': 7,
            'Major': 8,
            'Capitão': 9,
            'Primeiro Tenente': 10,
            'Segundo Tenente': 11,
            'Cadete': 12,
            'Subtenente': 13,
            'Primeiro Sargento': 14,
            'Segundo Sargento': 15,
            'Terceiro Sargento': 16,
            'Aluno': 17,
            'Cabo': 18,
            'Especialista': 19,
            'Soldado 1ª Classe': 20,
            'Soldado': 21,
        }
        # Definir a ordem da patente com base no mapa
        self.patente_order = patente_order_map.get(self.patente, 99)

        # Gerar slug a partir do username se o slug estiver vazio
        if not self.slug:
            base_slug = slugify(self.username)
            slug = base_slug
            n = 1
            while MilitarUsuario.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug

        # Chamar o método save() da superclasse
        super().save(*args, **kwargs)

    def __str__(self):
            return f"{self.username}, {self.patente}"