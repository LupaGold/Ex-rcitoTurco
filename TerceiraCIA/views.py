from django.shortcuts import render
from ConAcs.views import PatenteRequiredMixin
from django.db.models import Count, F
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView
from .models import Destaque3CIA, Doação3CIA, Relatório3CIA
from django.utils import timezone
from datetime import timedelta
from .forms import Doação3CIAForm, Destaque3CIAForm, Relatório3CIAForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.urls import reverse

class CriarDestaque3CIA(CreateView):
    template_name = 'Form.html'
    form_class = Destaque3CIAForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.datatime = timezone.now()
            form.save()
            return HttpResponseRedirect(reverse('Relatório3CIA'))
        else:
            return self.get(request, *args, **kwargs)

class Relatório3CIAView(ListView):
    model = Relatório3CIA
    template_name = 'Relatório3CIA.html'
    context_object_name = 'relatorios'

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = Relatório3CIA.objects.all()

        if q:
            queryset = queryset.filter(resp__username__icontains=q)

        return queryset.order_by('-data')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_atual = timezone.now()
        
        # Calcular a data e hora da última segunda-feira
        ultima_segunda = (data_atual - timedelta(days=data_atual.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Calcular a data e hora da próxima segunda-feira
        proxima_segunda = (ultima_segunda + timedelta(days=7))

        # Calcular o tempo restante para a próxima segunda-feira
        tempo_falta = proxima_segunda - data_atual
        dias_falta = tempo_falta.days
        segundos_restantes = tempo_falta.seconds

        horas_falta = segundos_restantes // 3600
        minutos_falta = (segundos_restantes % 3600) // 60
        segundos_falta = segundos_restantes % 60
        

        context['contador'] = Relatório3CIA.objects.filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        ).values('resp').annotate(total_3cia=Count('resp'))
        context['total'] = Relatório3CIA.objects.filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        ).count()
        # Agregação dos dados para contar o número de palestras enviadas por cada treinador
        ranking = (
            Relatório3CIA.objects
            .filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        )
            .values('resp__username')
            .annotate(total_3cia=Count('resp'))
            .order_by('-total_3cia')
        )

        # Convertemos o QuerySet para uma lista de dicionários
        context['destaque'] = Destaque3CIA.objects.last()
        context['ranking'] = ranking
        context['dias_falta'] = dias_falta
        context['horas_falta'] = horas_falta
        context['minutos_falta'] = minutos_falta
        context['segundos_falta'] = segundos_falta
        return context

class Doação3CIAView(ListView):
    model = Doação3CIA
    template_name = 'Doação3CIA.html'
    context_object_name = 'relatorios'

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = Doação3CIA.objects.all()

        if q:
            queryset = queryset.filter(solicitante__username__icontains=q)

        return queryset.order_by('-data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_atual = timezone.now()
        
        # Calcular a data e hora da última segunda-feira
        ultima_segunda = (data_atual - timedelta(days=data_atual.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Calcular a data e hora da próxima segunda-feira
        proxima_segunda = (ultima_segunda + timedelta(days=7))

        # Calcular o tempo restante para a próxima segunda-feira
        tempo_falta = proxima_segunda - data_atual
        dias_falta = tempo_falta.days
        segundos_restantes = tempo_falta.seconds

        horas_falta = segundos_restantes // 3600
        minutos_falta = (segundos_restantes % 3600) // 60
        segundos_falta = segundos_restantes % 60

        context['contador'] = Doação3CIA.objects.filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        ).values('id').annotate(total_2cia=Count('id'))
        context['total'] = Doação3CIA.objects.filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        ).count()
        # Agregação dos dados para contar o número de palestras enviadas por cada treinador
        ranking = (
            Doação3CIA.objects
            .filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        )
            .values('solicitante__username')
            .annotate(total_3cia=Count('solicitante'))
            .order_by('-total_3cia')
        )

        # Convertemos o QuerySet para uma lista de dicionários
        context['destaque'] = Destaque3CIA.objects.last()
        context['ranking'] = ranking
        context['dias_falta'] = dias_falta
        context['horas_falta'] = horas_falta
        context['minutos_falta'] = minutos_falta
        context['segundos_falta'] = segundos_falta
        return context

class RegistrarDoação3CIA(CreateView):
    form_class = Doação3CIAForm
    template_name = 'Form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar Doação!'
        context["image"] = '3cia.gif'
        context["descricao"] = 'Verifique todos os campos antes de registrar a avaliação!'
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.data = timezone.now()
            form.save()

            return HttpResponseRedirect(reverse('Doação3CIA'))
        else:
            return self.get(request, *args, **kwargs)
        
class RegistrarRelatório3CIA(CreateView):
    form_class = Relatório3CIAForm
    template_name = 'Form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar Relatório'
        context["image"] = '3cia.gif'
        context["descricao"] = 'Verifique todos os campos antes de registrar o relatório!'
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.solicitante = request.user
            form.instance.data = timezone.now()
            form.save()

            return HttpResponseRedirect(reverse('Relatório3CIA'))
        else:
            return self.get(request, *args, **kwargs)