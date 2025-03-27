from django.shortcuts import render
from ConAcs.views import PatenteRequiredMixin
from django.db.models import Count, F
from Militares.models import MilitarUsuario
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView
from .models import Destaque3CIA, Doação3CIA, Relatório3CIA
from django.utils import timezone
from datetime import timedelta
from .forms import Doação3CIAForm, Destaque3CIAForm, Relatório3CIAForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404, redirect

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
        
@method_decorator(csrf_protect, name='dispatch')
class AdicionarL3CIA(PatenteRequiredMixin,View):
    allowed_groups = ['L3CIA'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
        ]
    template_name = 'Guia.html'
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        group = Group.objects.get(name='L3CIA')
        user.groups.add(group)
        return redirect('Permi3CIA')

@method_decorator(csrf_protect, name='dispatch')
class RemoverL3CIA(PatenteRequiredMixin,View):
    allowed_groups = ['L3CIA'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
        ]
    template_name = 'Guia.html'
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        group = Group.objects.get(name='L3CIA')
        user.groups.remove(group)
        return redirect('Permi3CIA')
    
@method_decorator(csrf_protect, name='dispatch')
class AdicionarM3CIA(PatenteRequiredMixin,View):
    allowed_groups = ['L3CIA'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
        ]
    template_name = 'Guia.html'
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        group = Group.objects.get(name='M3CIA')
        user.groups.add(group)
        return redirect('Permi3CIA')

@method_decorator(csrf_protect, name='dispatch')
class RemoverM3CIA(PatenteRequiredMixin,View):
    allowed_groups = ['L3CIA'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
        ]
    template_name = 'Guia.html'
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        group = Group.objects.get(name='M3CIA')
        user.groups.remove(group)
        return redirect('Permi3CIA')
    
class Permissoes3ciaview(PatenteRequiredMixin, ListView):
    allowed_groups = ['L3CIA'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
        ]
    template_name = 'Guia.html'
    model = MilitarUsuario
    template_name = 'Permi3cia.html'
    context_object_name = 'militares'
    paginate_by = 5

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = MilitarUsuario.objects.exclude(
            patente__in=[
                'Marechal ★★★★★',
                'General-de-Exército ★★★★',
                'General-de-Divisão ★★★',
                'General-de-Brigada ★★',
                'Coronel ★',
            ]
        ).order_by('patente_order')

        if q:
            queryset = queryset.filter(username__icontains=q).order_by('patente_order')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        grupos = Group.objects.all()

        for militar in context['militares']:
            militar.isl3 = 'L3CIA' in [group.name for group in militar.groups.all()]
            militar.ism3 = 'M3CIA' in [group.name for group in militar.groups.all()]

        context.update({
            'groups': grupos,
        })
        return context