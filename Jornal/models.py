from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

class PostagemJornal(models.Model):
    #Categorias de postagens
    CATEGORIAS = (
          ('Aposentadorias','Aposentadorias'),
          ('Promoções','Promoções'),
          ('Inaugurações','Inaugurações'),
          ('Formaturas','Formaturas'),
          ('Novidades','Novidades'),
    )
    #Jornalista responsável pela postagem
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantepostagem')
    #Título da postagem
    titulo = models.TextField(blank=False, null=True, max_length=30)
    #Categoria da postagem
    categoria = models.CharField(choices=CATEGORIAS,blank=False, null=True, max_length=30)
    #Descrição
    descricao = models.TextField(blank=False, null=True, max_length=70)
    #Treinamento escrito no Editor de texto
    texto = CKEditor5Field('Postagem', config_name='extends', default=' ')
    #Data e tempo de atualização do treinamento
    datatime = models.DateTimeField(default=timezone.now)
    #Imagem do banner da postagem
    imagem = models.ImageField(upload_to='imagens/')
    # Slug para URL amigável
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Postagem ({self.titulo} postado por {self.solicitante.username} em {self.datatime})'
    
class LogPostagem(models.Model):
      #Treinamento relacionado a log
      treinamento = models.ForeignKey(PostagemJornal, verbose_name=("postagem"), on_delete=models.PROTECT, null=True)
      #Texto da log
      texto = models.TextField(blank=False, null=True, verbose_name='Texto postagem', max_length=150)
      #Data e tempo de criação da log
      datatime = models.DateTimeField(default=timezone.now)
