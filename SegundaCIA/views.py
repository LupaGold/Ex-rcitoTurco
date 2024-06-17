from django.shortcuts import render
from ConAcs.views import PatenteRequiredMixin
from django.db.models import Count, F
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView
from .models import AvaliaçãoTP, Relatório2CIA, Destaque2CIA
from django.utils import timezone
from datetime import timedelta
from .forms import AvaliaçãoTPForm, Relatório2CIAForm, Destaque2CIAForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.urls import reverse

class CriarDestaque2CIA(PatenteRequiredMixin,CreateView):
    allowed_groups = ['L2CIA'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    template_name = 'Form.html'
    form_class = Destaque2CIAForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.datatime = timezone.now()
            form.save()
            return HttpResponseRedirect(reverse('AvaliaçãoTP'))
        else:
            return self.get(request, *args, **kwargs)

class AvaliaçãoTPView(PatenteRequiredMixin,ListView):
    allowed_groups = ['L2CIA', 'M2CIA'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    model = AvaliaçãoTP
    template_name = 'AvaliaçãoTP.html'
    context_object_name = 'relatorios'

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = AvaliaçãoTP.objects.all()

        if q:
            queryset = queryset.filter(treinador_nick__icontains=q)

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
        

        context['contador'] = AvaliaçãoTP.objects.filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        ).values('tp').annotate(total_2cia=Count('tp'))
        context['total'] = AvaliaçãoTP.objects.filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        ).count()
        # Agregação dos dados para contar o número de palestras enviadas por cada treinador
        ranking = (
            AvaliaçãoTP.objects
            .filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        )
            .values('solicitante')
            .annotate(total_2cia=Count('solicitante'),
                      solicitante__username=F('solicitante__username'))
            .order_by('-total_2cia')
        )

        # Convertemos o QuerySet para uma lista de dicionários
        context['destaque'] = Destaque2CIA.objects.last()
        context['ranking'] = ranking
        context['dias_falta'] = dias_falta
        context['horas_falta'] = horas_falta
        context['minutos_falta'] = minutos_falta
        context['segundos_falta'] = segundos_falta
        return context

class Relatório2CIAView(PatenteRequiredMixin,ListView):
    allowed_groups = ['L2CIA', 'M2CIA'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    model = Relatório2CIA
    template_name = 'Relatório2CIA.html'
    context_object_name = 'relatorios'

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = Relatório2CIA.objects.all()

        if q:
            queryset = queryset.filter(treinador_nick__icontains=q)

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

        context['contador'] = Relatório2CIA.objects.filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        ).values('id').annotate(total_2cia=Count('id'))
        context['total'] = Relatório2CIA.objects.filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        ).count()
        # Agregação dos dados para contar o número de palestras enviadas por cada treinador
        ranking = (
            Relatório2CIA.objects
            .filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        )
            .values('avaliador__username')
            .annotate(total_2cia=Count('avaliador'))
            .order_by('-total_2cia')
        )

        # Convertemos o QuerySet para uma lista de dicionários
        context['destaque'] = Destaque2CIA.objects.last()
        context['ranking'] = ranking
        context['dias_falta'] = dias_falta
        context['horas_falta'] = horas_falta
        context['minutos_falta'] = minutos_falta
        context['segundos_falta'] = segundos_falta
        return context

class RegistrarTP(PatenteRequiredMixin,CreateView):
    allowed_groups = ['L2CIA', 'M2CIA'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    form_class = AvaliaçãoTPForm
    template_name = 'Form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar Avaliação TP'
        context["image"] = '2cia.gif'
        context["descricao"] = 'Verifique todos os campos antes de registrar a avaliação!'
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.data = timezone.now()
            form.save()

            return HttpResponseRedirect(reverse('AvaliaçãoTP'))
        else:
            return self.get(request, *args, **kwargs)
        
class RegistrarRelatório2CIA(PatenteRequiredMixin,CreateView):
    allowed_groups = ['L2CIA', 'M2CIA'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    form_class = Relatório2CIAForm
    template_name = 'Form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar Relatório'
        context["image"] = '2cia.gif'
        context["descricao"] = 'Verifique todos os campos antes de registrar o relatório!'
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.data = timezone.now()
            form.save()

            return HttpResponseRedirect(reverse('Relatório2CIA'))
        else:
            return self.get(request, *args, **kwargs)