from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from .models import PostagemJornal
from Militares.models import MilitarUsuario
from django.contrib.auth.models import Group

class JornalPrincipal(TemplateView):
    template_name = 'PrincipalJornal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Grupo de Jornalista 
        membro = 'JORNALISTA'
        #Lógica para testar os Militares se fazem parte dos grupos
        try:
            grupo_membro = Group.objects.get(name=membro)
            context['membros'] = MilitarUsuario.objects.filter(groups=grupo_membro).order_by('patente_order')
        except Group.DoesNotExist:
            context['membros'] = MilitarUsuario.objects.none()

        context["postagens"] = PostagemJornal.objects.all().order_by('-datatime')[:2]
        return context
    

#View para ver as postagens individualmente
class Postagens(DetailView):
    model = PostagemJornal
    template_name = 'PostagensJornal.html'
    context_object_name = 'postagem'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context