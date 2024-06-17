from django.views.generic import TemplateView, ListView, DetailView, View, CreateView
from .models import RelatoriosDeTreinamento, LogRelatorio
from .forms import RelatorioDeTreinamentoForm
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from ConAcs.views import PatenteRequiredMixin


# View de relatórios
User = get_user_model()

class RelatorioPraça(PatenteRequiredMixin,TemplateView):
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
            
            # Filtrar usuários com as patentes desejadas
            patentes_desejadas = ['Aspirante-a-Oficial','Segundo Tenente','Primeiro Tenente','Capitão','Major', 'Tenente-Coronel']
            usuarios = User.objects.filter(patente__in=patentes_desejadas)
            
            # Enviar notificações via Channels
            channel_layer = get_channel_layer()
            
            for usuario in usuarios:
                async_to_sync(channel_layer.group_send)(
                    f"user_{usuario.id}",
                    {
                        "type": "send_notification",
                        "message": f"Atenção um relatório foi enviado por {relatorio.solicitante.username}."
                    }
                )
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
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
            'Tenente-Coronel',
            'Major',
            'Capitão',
            'Segundo Tenente',
            'Primeiro Tenente',
            'Aspirante-a-Oficial',
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
        context['contador'] = RelatoriosDeTreinamento.objects.all().values('treinamento').annotate(total=Count('treinamento'))
        context['total'] = RelatoriosDeTreinamento.objects.all().count()
        return context
    
class AprovarRelatorio(PatenteRequiredMixin,View):
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
        
        # Enviar notificação
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{relatorio.solicitante.id}",
            {
                "type": "send_notification",
                "message": f"O seu relatório de treinamento foi aprovado."
            }
        )

        return HttpResponseRedirect(reverse('RelatoriosOficiais'))

class ReprovarRelatorio(PatenteRequiredMixin,View):
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
        
        # Enviar notificação
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{relatorio.solicitante.id}",
            {
                "type": "send_notification",
                "message": f"O seu relatório de treinamento foi reprovado."
            }
        )

        return HttpResponseRedirect(reverse('RelatoriosOficiais'))