from django.shortcuts import render
from django.views.generic import TemplateView
from Treinamentos.models import RelatoriosDeTreinamento
from django.db.models import Count
from Militares.models import MilitarUsuario
from Forum.models import Post
from Forum.forms import PostForm, ComentarioForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import FormMixin
from Honrarias.models import HonrariaMilitar
from ConAcs.views import PatenteRequiredMixin
from Loja.models import EmblemasModel
#View da página principal do site
class PrincipalView(PatenteRequiredMixin,TemplateView, FormMixin):
    allowed_groups = [] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
            'Tenente-Coronel',
            'Major',
            'Capitão',
            'Segundo Tenente',
            'Primeiro Tenente',
            'Aspirante-a-Oficial',
            'Cadete',
            'Subtenente',
            'Primeiro Sargento',
            'Segundo Sargento',
            'Terceiro Sargento',
            'Aluno',
        ]
    template_name = 'PrincipalPainel.html'
    paginate_by = 5
    model = Post
    context_object_name = 'posts'
    form_class = PostForm
    comentario_form_class = ComentarioForm

    def post(self, request, *args, **kwargs):
        if 'post_id' in request.POST:  # Identifica o formulário de comentário
            comentario_form = self.comentario_form_class(request.POST)
            if comentario_form.is_valid():
                comentario_form.instance.autor = self.request.user
                comentario_form.instance.post_id = request.POST.get('post_id')
                comentario_form.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.form_invalid(comentario_form)
        else:
            form = self.get_form()
            if form.is_valid():
                form.instance.autor = self.request.user
                form.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.form_invalid(form)

    def get_success_url(self):
        return reverse('PrincipalPainel')

    def get(self, request, *args, **kwargs):
        search_term = request.GET.get('search', '') 
        militar = MilitarUsuario.objects.filter(username__icontains=search_term) if search_term else None
        honrarias = HonrariaMilitar.objects.filter(militar__username__icontains=search_term)

        context = {
            'form': self.get_form(),
            'posts': Post.objects.all().order_by('-data'),
            'comentario_form': self.comentario_form_class(),
            'militar': militar,
            'busca': search_term,
            'TreinamentosContador':RelatoriosDeTreinamento.objects.filter(solicitante=self.request.user).count(),
            'AuxilioContador': RelatoriosDeTreinamento.objects.filter(auxiliar=self.request.user.username).count(),
            'honrarias': honrarias,
            'emblema': EmblemasModel.objects.last(),
        }
        return self.render_to_response(context)

    
