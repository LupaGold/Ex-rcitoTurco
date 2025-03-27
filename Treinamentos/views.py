from django.views.generic import TemplateView, ListView, DetailView, View, CreateView
from .models import RelatoriosDeTreinamento, LogRelatorio
from .forms import RelatorioDeTreinamentoForm
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from ConAcs.views import PatenteRequiredMixin
from django.utils import timezone
from datetime import timedelta

# View de relatórios
User = get_user_model()

class RelatorioPraça(PatenteRequiredMixin,TemplateView):
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
    model = RelatoriosDeTreinamento
    template_name = 'RelatoriosPraças.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['relatorios'] = RelatoriosDeTreinamento.objects.filter(solicitante=self.request.user).order_by('-data')
        context['contador'] = RelatoriosDeTreinamento.objects.filter(solicitante=self.request.user).values('treinamento').annotate(total=Count('treinamento'))
        context['total'] = RelatoriosDeTreinamento.objects.filter(solicitante=self.request.user).count()
        return context

class RegistrarRelatorio(PatenteRequiredMixin,CreateView):
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
    form_class = RelatorioDeTreinamentoForm
    template_name = 'FormRelatorioDeTreinamento.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar Relatório'
        context["image"] = 'relatorio.png'
        context["descricao"] = 'Verifique todos os campos antes de enviar o relatório!'
        return context
    

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.solicitante = self.request.user
            relatorio = form.save()

            # Incrementar moedas do solicitante
            solicitante = relatorio.solicitante
            solicitante.moedas += 0.2
            solicitante.save()
            
            log = LogRelatorio.objects.create(
                    relatorio=relatorio,
                    texto=f"{relatorio.solicitante} enviou um relatório de treinamento!",
                    datatime=timezone.now(),
                )

            log.save()

            return HttpResponseRedirect(reverse('AvalPraça'))
        else:
            return self.get(request, *args, **kwargs)
        
class RelatorioOficial(PatenteRequiredMixin, ListView):
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
    model = RelatoriosDeTreinamento
    template_name = 'RelatoriosOficiais.html'
    context_object_name = 'relatorios'

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = RelatoriosDeTreinamento.objects.all()

        if q:
            queryset = queryset.filter(treinador__icontains=q)

        queryset = queryset.order_by('-data')

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_atual = timezone.now()
        # Calcular a data e hora da última segunda-feira
        ultima_segunda = (data_atual - timedelta(days=data_atual.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Calcular a data e hora da próxima segunda-feira
        proxima_segunda = (ultima_segunda + timedelta(days=7))
        ranking = (
            RelatoriosDeTreinamento.objects
            .filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        )
            .values('treinador')
            .annotate(total=Count('id'))
            .order_by('-total')
        )
        context['contador'] = RelatoriosDeTreinamento.objects.all().values('treinamento').annotate(total=Count('treinamento'))
        context['total'] = RelatoriosDeTreinamento.objects.all().count()
        context['ranking'] = ranking
        return context
    
class AprovarRelatorio(PatenteRequiredMixin,View):
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
    def post(self, request, *args, **kwargs):
        relatorio_id = kwargs.get('relatorio_id')
        relatorio = get_object_or_404(RelatoriosDeTreinamento, id=relatorio_id)
        relatorio.status = 'Aprovado'
        relatorio.aprovador = request.user
        relatorio.save()

        LogRelatorio.objects.create(
            relatorio=relatorio,
            texto=f'O Relatório de treinamento enviado por {relatorio.solicitante.patente} {relatorio.solicitante.username} foi aprovado por {request.user.username}.',
            datatime=timezone.now()
        )
        

        return HttpResponseRedirect(reverse('RelatoriosOficiais'))

class ReprovarRelatorio(PatenteRequiredMixin,View):
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
    def post(self, request, *args, **kwargs):
        relatorio_id = kwargs.get('relatorio_id')
        relatorio = get_object_or_404(RelatoriosDeTreinamento, id=relatorio_id)
        relatorio.status = 'Reprovado'
        relatorio.aprovador = request.user
        relatorio.save()

        LogRelatorio.objects.create(
            relatorio=relatorio,
            texto=f'O Relatório de treinamento enviado por {relatorio.solicitante.patente} {relatorio.solicitante.username} foi reprovado por {request.user.username}.',
            datatime=timezone.now()
        )
        

        return HttpResponseRedirect(reverse('RelatoriosOficiais'))