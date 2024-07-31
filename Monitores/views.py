from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView, UpdateView
from .models import MonitorRelatorio, GuiaMonitores, DestaqueMonitores
from django.db.models import Count
from .forms import GuiaMonitoresForm, MonitorForm, DestaqueMonitoresForm
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
import logging
from Militares.models import MilitarUsuario
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from ConAcs.views import PatenteRequiredMixin

logger = logging.getLogger(__name__)

# Create your views here.
class MonitorPraça(PatenteRequiredMixin,TemplateView):
    allowed_groups = ['MNT', 'RMNT', 'LMNT'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    model = MonitorRelatorio
    template_name = 'MonitoresPraças.html'

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

        context['relatorios'] = MonitorRelatorio.objects.filter(solicitante=self.request.user).order_by('-data')
        context['contador'] = MonitorRelatorio.objects.filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        ).values('treinamento').annotate(total=Count('treinamento'))
        context['total'] = MonitorRelatorio.objects.filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        ).count()
        # Agregação dos dados para contar o número de palestras enviadas por cada treinador
        ranking = (
            MonitorRelatorio.objects
            .filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        )
            .values('treinador_nick')
            .annotate(total_treinamento=Count('id'))
            .order_by('-total_treinamento')
        )

        # Convertemos o QuerySet para uma lista de dicionários
        context['destaque'] = DestaqueMonitores.objects.last()
        context['ranking'] = ranking
        context['dias_falta'] = dias_falta
        context['horas_falta'] = horas_falta
        context['minutos_falta'] = minutos_falta
        context['segundos_falta'] = segundos_falta


        return context
    
class GuiaMonitoresEdit(PatenteRequiredMixin,UpdateView):
    allowed_groups = ['RMNT', 'LMNT'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    model = GuiaMonitores
    form_class = GuiaMonitoresForm
    template_name = 'Form.html'
    success_url = reverse_lazy('GuiaMonitores')

class GuiaMonitoresView(PatenteRequiredMixin,TemplateView):
    allowed_groups = ['MNT', 'RMNT', 'LMNT'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    template_name = 'Guia.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["guia"] = GuiaMonitores.objects.last()
        return context

class CriarDestaqueMonitores(PatenteRequiredMixin,CreateView):
    allowed_groups = ['LMNT'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    template_name = 'Form.html'
    form_class = DestaqueMonitoresForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.data = timezone.now()
            form.save()
            return HttpResponseRedirect(reverse('MonitoresOficiais'))
        else:
            return self.get(request, *args, **kwargs)
        
@method_decorator(csrf_protect, name='dispatch')
class AdicionarMNTView(PatenteRequiredMixin,View):
    allowed_groups = ['RMNT', 'LMNT'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        group = Group.objects.get(name='MNT')
        user.groups.add(group)
        return redirect('PermissoesMNT')

@method_decorator(csrf_protect, name='dispatch')
class RemoverMNTView(PatenteRequiredMixin,View):
    allowed_groups = ['RMNT', 'RMNT'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        group = Group.objects.get(name='MNT')
        user.groups.remove(group)
        return redirect('PermissoesMNT')
    
@method_decorator(csrf_protect, name='dispatch')
class AdicionarRMNTView(PatenteRequiredMixin,View):
    allowed_groups = ['LMNT'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        group = Group.objects.get(name='RMNT')
        user.groups.add(group)
        return redirect('PermissoesMNT')

@method_decorator(csrf_protect, name='dispatch')
class RemoverRMNTView(PatenteRequiredMixin,View):
    allowed_groups = ['LMNT'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        group = Group.objects.get(name='RMNT')
        user.groups.remove(group)
        return redirect('PermissoesMNT')
    
@method_decorator(csrf_protect, name='dispatch')
class AdicionarLMNTView(PatenteRequiredMixin,View):
    allowed_groups = ['LMNT'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        group = Group.objects.get(name='LMNT')
        user.groups.add(group)
        return redirect('PermissoesMNT')

@method_decorator(csrf_protect, name='dispatch')
class RemoverLMNTView(PatenteRequiredMixin,View):
    allowed_groups = ['LMNT'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        group = Group.objects.get(name='LMNT')
        user.groups.remove(group)
        return redirect('PermissoesMNT')
    
class RegistrarRelatorioMonitores(PatenteRequiredMixin,CreateView):
    allowed_groups = ['MNT', 'RMNT', 'LMNT'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    form_class = MonitorForm
    template_name = 'Form.html'
    success_url = reverse_lazy('MonitoresPraça')

    
    def form_valid(self, form):
        sup = form.save(commit=False)
        sup.solicitante = self.request.user
        sup.data = timezone.now()
        sup.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar ação de Monitores!'
        context["image"] = 'monitores.gif'
        context["descricao"] = 'Verifique todos os campos antes de enviar o relatório!'
        return context
    
class MonitorOficial(PatenteRequiredMixin,ListView):
    allowed_groups = ['RMNT', 'LMNT'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    model = MonitorRelatorio
    template_name = 'MonitoresOficiais.html'
    context_object_name = 'relatorios'

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = MonitorRelatorio.objects.all()

        if q:
            queryset = queryset.filter(treinador__icontains=q)

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

        context['contador'] = MonitorRelatorio.objects.filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        ).values('treinamento').annotate(total=Count('treinamento'))
        context['total'] = MonitorRelatorio.objects.filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        ).count()
        # Agregação dos dados para contar o número de palestras enviadas por cada treinador
        ranking = (
            MonitorRelatorio.objects
            .filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        )
            .values('treinador_nick')
            .annotate(total_palestras=Count('id'))
            .order_by('-total_palestras')
        )

        # Convertemos o QuerySet para uma lista de dicionários
        context['destaque'] = DestaqueMonitores.objects.last()
        context['ranking'] = ranking
        context['dias_falta'] = dias_falta
        context['horas_falta'] = horas_falta
        context['minutos_falta'] = minutos_falta
        context['segundos_falta'] = segundos_falta
        return context
    
class PermissoesMNTView(PatenteRequiredMixin ,ListView):
    allowed_groups = ['RMNT', 'LMNT'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    model = MilitarUsuario
    template_name = 'PermissõesMonitores.html'
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
        )

        if q:
            queryset = queryset.filter(username__icontains=q)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        grupos = Group.objects.all()

        for militar in context['militares']:
            militar.is_sup = 'MNT' in [group.name for group in militar.groups.all()]
            militar.is_rsup = 'RMNT' in [group.name for group in militar.groups.all()]
            militar.is_lsup = 'LMNT' in [group.name for group in militar.groups.all()]

        context.update({
            'groups': grupos,
        })
        return context