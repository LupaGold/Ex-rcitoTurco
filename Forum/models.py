from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

#Model do post do fórum
class Post(models.Model):
      #Data do post
      data = models.DateTimeField(blank=False, null=True, default=timezone.now)
      #Autor do post
      autor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True)
      #Texto do post
      texto = models.TextField(blank=False, null=True, verbose_name='Texto', max_length=150)
      
      def __str__(self):
        return str(self.autor)

#Model dos comentarios de post do forum
class Comentario(models.Model):
    #Data do comentario
    data = models.DateTimeField(blank=False, null=True, default=timezone.now)
    #Post vinculado
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    #Autor do comentário
    autor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='comentarioautor')
    #Texto do post
    texto = models.TextField()