from django.shortcuts import render
from ConAcs.views import PatenteRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView
from .models import Re, LogRE, RM
from .forms import ReForm, RMForm
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
# View de relatórios
User = get_user_model()

class RePraça(PatenteRequiredMixin,ListView):
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
    model = Re
    template_name = 'RePraça.html'
    context_object_name = 'recrutamentos'

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = Re.objects.all()

        if q:
            queryset = queryset.filter(militar__icontains=q)

        return queryset.order_by('-data')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_atual = timezone.now()
        # Calcular a data e hora da última segunda-feira
        ultima_segunda = (data_atual - timedelta(days=data_atual.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)

        # Calcular a data e hora da próxima segunda-feira
        proxima_segunda = (ultima_segunda + timedelta(days=7))
        ranking = (
            Re.objects
            .filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        )
            .values('militar')
            .annotate(total=Count('id'))
            .order_by('-total')
        )
        context['ranking'] = ranking
        context['recrutamentos'] = Re.objects.all().order_by('-data')
        return context

class AbrirRE(PatenteRequiredMixin,CreateView):
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
    form_class = ReForm
    template_name = 'Form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Abrir Relatório de Recrutamento'
        context["image"] = 're.gif'
        context["descricao"] = 'Verifique todos os campos antes de enviar o relatório!'
        return context


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.data = timezone.now()
            relatorio = form.save()

            # Incrementar moedas do solicitante
            solicitante = relatorio.solicitante
            solicitante.moedas += 1
            solicitante.save()

            log = LogRE.objects.create(
                    re=relatorio,
                    texto=f"{relatorio.solicitante} enviou abriu um Recrutamento Externo!",
                    datatime=timezone.now(),
                )

            log.save()

            return HttpResponseRedirect(reverse('RePraça'))
        else:
            return self.get(request, *args, **kwargs)

class AbrirRM(PatenteRequiredMixin,CreateView):
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
    form_class = RMForm
    template_name = 'Form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Abrir Relatório de Movimento'
        context["image"] = 'oficiais.gif'
        context["descricao"] = 'Verifique todos os campos antes de enviar o relatório!'
        return context


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.data = timezone.now()
            form.save()


            return HttpResponseRedirect(reverse('PrincipalPainel'))
        else:
            return self.get(request, *args, **kwargs)

class RMOficial(PatenteRequiredMixin,ListView):
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
    model = RM
    template_name = 'RM.html'
    context_object_name = 'recrutamentos'

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = Re.objects.all()

        if q:
            queryset = queryset.filter(militar__icontains=q)

        return queryset.order_by('-data')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recrutamentos'] = RM.objects.all().order_by('-data')
        return context