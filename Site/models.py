from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

#Model de páginas
class PaginaSite(models.Model):
    #Categorias de paginas
    CATEGORIAS = (
          ('Grupos','Grupos'),
          ('Apostilas','Apostilas'),
          ('Escolas e Institutos','Escolas e Institutos'),
          ('Team Speak','Team Speak'),
          ('Hierarquia','Hierarquia'),
    )
    #Militar responsável pela alteração na pagina
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantepágina')
    #Título da pagina
    titulo = models.TextField(blank=False, null=True, max_length=30)
    #Categoria da pagina
    categoria = models.CharField(choices=CATEGORIAS,blank=False, null=True, max_length=30)
    #Descrição da pagina
    descricao = models.TextField(blank=False, null=True, max_length=70)
    #Treinamento escrito no Editor de texto
    texto = CKEditor5Field('Postagem', config_name='extends', default=' ')
    #Data e tempo de atualização da pagina
    datatime = models.DateTimeField(default=timezone.now)
    #Icone do banner da pagina
    icone = models.ImageField(upload_to='imagens/')
    # Slug para URL amigável
    slug = models.SlugField(unique=True, blank=True, null=True)
    # Campo para ordenar as paginas
    ordenador = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Página ({self.titulo} alterada/criada por {self.solicitante.username} em {self.datatime})'
    
class LogPáginas(models.Model):
      #Treinamento relacionado a log
      treinamento = models.ForeignKey(PaginaSite, verbose_name=("paginas"), on_delete=models.PROTECT, null=True)
      #Texto da log
      texto = models.TextField(blank=False, null=True, verbose_name='Texto paginas', max_length=150)
      #Data e tempo de criação da log
      datatime = models.DateTimeField(default=timezone.now)

class Aviso(models.Model):
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitanteaviso')
    texto = models.TextField(blank=False, null=True, max_length=300)
    datatime = models.DateTimeField(default=timezone.now)