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
from .models import Documentos
from Recrutamento.models import Re
from django.utils import timezone
from Recrutamento.models import Re
from Ajudantes.models import AjudanteRelatorio
from Monitores.models import MonitorRelatorio
from Supervisores.models import SupervisorRelatorio
from Treinamentos.models import RelatoriosDeTreinamento
#View da página principal do site
class PrincipalView(PatenteRequiredMixin,TemplateView, FormMixin):
    allowed_groups = []
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
            'Coronel',
            'Tenente-Coronel',
            'Major',
            'Capitão',
            'Segundo Tenente',
            'Primeiro Tenente',
            'Cadete',
            'Sargento Major',
            'Sargento Mestre',
            'Sargento Staff',
            'Sargento',
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
        data_de_hoje = timezone.now().date()

        context = {
            'form': self.get_form(),
            'posts': Post.objects.all().order_by('-data'),
            'comentario_form': self.comentario_form_class(),
            'militar': militar,
            'busca': search_term,
            'TreinamentosContador': RelatoriosDeTreinamento.objects.filter(data__date=data_de_hoje).count(),
            'AuxilioContador': RelatoriosDeTreinamento.objects.filter(data__date=data_de_hoje).exclude(auxiliar='').count(),
            'REContador': Re.objects.filter(data__date=data_de_hoje).count(),
            'honrarias': honrarias,
            'emblema': EmblemasModel.objects.last(),
        }
        return self.render_to_response(context)

class RegimentoView(PatenteRequiredMixin,TemplateView):
    allowed_groups = []
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
            'Coronel',
            'Tenente-Coronel',
            'Major',
            'Capitão',
            'Segundo Tenente',
            'Primeiro Tenente',
        ]
    template_name = 'Guia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["guia"] = Documentos.objects.filter(categoria='Regimento').last()
        return context

class InfoView(PatenteRequiredMixin,TemplateView):
    allowed_groups = []
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
            'Coronel',
            'Tenente-Coronel',
            'Major',
            'Capitão',
            'Segundo Tenente',
            'Primeiro Tenente',
        ]
    template_name = 'Guia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["guia"] = Documentos.objects.filter(categoria='Informações').last()
        return context

class FAQView(PatenteRequiredMixin,TemplateView):
    allowed_groups = []
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
            'Coronel',
            'Tenente-Coronel',
            'Major',
            'Capitão',
            'Segundo Tenente',
            'Primeiro Tenente',
        ]
    template_name = 'Guia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["guia"] = Documentos.objects.filter(categoria='FAQ').last()
        return context

class Ranking(PatenteRequiredMixin,TemplateView):
    allowed_groups = []
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
            'Coronel',
            'Tenente-Coronel',
            'Major',
            'Capitão',
            'Segundo Tenente',
            'Primeiro Tenente',
        ]
    template_name = 'Ranking.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rankingajd = (
                AjudanteRelatorio.objects
                .all()
                .values('treinador')
                .annotate(total_palestras=Count('id'))
                .order_by('-total_palestras')[:5]
            )
        rankingmnt = (
                MonitorRelatorio.objects
                .all()
                .values('treinador_nick')
                .annotate(total_treinamento=Count('id'))
                .order_by('-total_treinamento')[:5]
        )
        rankingsup = (
            SupervisorRelatorio.objects
            .all()
            .values('treinador')
            .annotate(total_palestras=Count('id'))
            .order_by('-total_palestras')[:5]
        )
        rankingre = (
            Re.objects
            .all()
            .values('militar')
            .annotate(total=Count('id'))
            .order_by('-total')[:5]
        )
        rankingtreinamento = (
            RelatoriosDeTreinamento.objects
            .all()
            .values('treinador')
            .annotate(total=Count('id'))
            .order_by('-total')[:5]
        )
        rankingauxilio = (
            RelatoriosDeTreinamento.objects
            .filter(auxiliar__isnull=False)
            .exclude(auxiliar='')
            .values('auxiliar')
            .annotate(total=Count('id'))
            .order_by('-total')[:5]
        )
        context["rankingauxilio"] = rankingauxilio
        context["rankingre"] = rankingre
        context["rankingtreinamento"] = rankingtreinamento
        context["rankingsup"] = rankingsup
        context["rankingajd"] = rankingajd
        context["rankingmnt"] = rankingmnt
        return context