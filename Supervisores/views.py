from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView, UpdateView
from .models import SupervisorRelatorio, DestaqueSupervisor, PalestraSupervisores, GuiaSupervisores
from django.db.models import Count
from .forms import SupervisorForm, PalestraSupervisoresForm, DestaqueSupervisorForm, GuiaSupervisoresForm
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

class SupervisoresPraça(PatenteRequiredMixin,TemplateView):
    allowed_groups = ['SUP', 'RSUP', 'LSUP'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
        ]
    model = SupervisorRelatorio
    template_name = 'SupervisoresPraça.html'

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

        context['relatorios'] = SupervisorRelatorio.objects.filter(solicitante=self.request.user).order_by('-datatime')
        context['contador'] = SupervisorRelatorio.objects.filter(
            datatime__gte=ultima_segunda,
            datatime__lt=proxima_segunda
        ).values('palestra__titulo').annotate(total=Count('palestra'))
        context['total'] = SupervisorRelatorio.objects.filter(
            datatime__gte=ultima_segunda,
            datatime__lt=proxima_segunda
        ).count()
        # Agregação dos dados para contar o número de palestras enviadas por cada treinador
        ranking = (
            SupervisorRelatorio.objects
            .filter(
            datatime__gte=ultima_segunda,
            datatime__lt=proxima_segunda
        )
            .values('treinador')
            .annotate(total_palestras=Count('id'))
            .order_by('-total_palestras')
        )

        # Convertemos o QuerySet para uma lista de dicionários
        context['destaque'] = DestaqueSupervisor.objects.last()
        context['ranking'] = ranking
        context['dias_falta'] = dias_falta
        context['horas_falta'] = horas_falta
        context['minutos_falta'] = minutos_falta
        context['segundos_falta'] = segundos_falta


        return context

class RegistrarRelatorioSupervisor(PatenteRequiredMixin,CreateView):
    allowed_groups = ['SUP', 'RSUP', 'LSUP'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
        ]
    form_class = SupervisorForm
    template_name = 'Form.html'
    success_url = reverse_lazy('SupervisoresPraça')

    def form_valid(self, form):
        sup = form.save(commit=False)
        sup.solicitante = self.request.user
        sup.datatime = timezone.now()
        sup.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar ação de Supervisor!'
        context["image"] = 'supervisores.gif'
        context["descricao"] = 'Verifique todos os campos antes de enviar o relatório!'
        return context
    
class SupSite(PatenteRequiredMixin,TemplateView):
    allowed_groups = ['SUP', 'RSUP', 'LSUP'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
        ]
    model = PalestraSupervisores
    template_name = 'SupervisoresPalestras.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Grupos Líder e Membro da 2CIA
        lider = 'LSUP'  
        membro = 'RSUP'
        #Lógica para testar os Militares se fazem parte dos grupos
        try:
            grupo_lider = Group.objects.get(name=lider)
            context['lider'] = MilitarUsuario.objects.filter(groups=grupo_lider).first()
        except Group.DoesNotExist:
            context['lider'] = MilitarUsuario.objects.none()
        
        try:
            grupo_membro = Group.objects.get(name=membro)
            context['membros'] = MilitarUsuario.objects.filter(groups=grupo_membro).order_by('patente_order')
        except Group.DoesNotExist:
            context['membros'] = MilitarUsuario.objects.none()

        context['treinamentos'] = PalestraSupervisores.objects.all()
        return context

class SupervisoresOficial(PatenteRequiredMixin,ListView):
    allowed_groups = ['RSUP', 'LSUP'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
        ]
    model = SupervisorRelatorio
    template_name = 'SupervisoresOficial.html'
    context_object_name = 'relatorios'

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = SupervisorRelatorio.objects.all()

        if q:
            queryset = queryset.filter(treinador__icontains=q)

        return queryset.order_by('-datatime')

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

        context['contador'] = SupervisorRelatorio.objects.filter(
            datatime__gte=ultima_segunda,
            datatime__lt=proxima_segunda
        ).values('palestra__titulo').annotate(total=Count('palestra'))
        context['total'] = SupervisorRelatorio.objects.filter(
            datatime__gte=ultima_segunda,
            datatime__lt=proxima_segunda
        ).count()
        # Agregação dos dados para contar o número de palestras enviadas por cada treinador
        ranking = (
            SupervisorRelatorio.objects
            .filter(
            datatime__gte=ultima_segunda,
            datatime__lt=proxima_segunda
        )
            .values('treinador')
            .annotate(total_palestras=Count('id'))
            .order_by('-total_palestras')
        )

        # Convertemos o QuerySet para uma lista de dicionários
        context['destaque'] = DestaqueSupervisor.objects.last()
        context['ranking'] = ranking
        context['dias_falta'] = dias_falta
        context['horas_falta'] = horas_falta
        context['minutos_falta'] = minutos_falta
        context['segundos_falta'] = segundos_falta
        return context
    
class PalestraSupervisoresUpdateView(PatenteRequiredMixin,UpdateView):
    allowed_groups = ['LSUP'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
        ]
    model = PalestraSupervisores
    form_class = PalestraSupervisoresForm
    template_name = 'Form.html'
    success_url = reverse_lazy('SupSite')

class GuiaSupervisoresEdit(PatenteRequiredMixin,UpdateView):
    allowed_groups = ['LSUP'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
        ]
    model = GuiaSupervisores
    form_class = GuiaSupervisoresForm
    template_name = 'Form.html'
    success_url = reverse_lazy('GuiaSupervisores')

class GuiaSupervisoresView(PatenteRequiredMixin,TemplateView):
    allowed_groups = ['SUP', 'RSUP', 'LSUP'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
        ]
    template_name = 'Guia.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["guia"] = GuiaSupervisores.objects.last()
        return context
    
class CriarDestaque(PatenteRequiredMixin,CreateView):
    allowed_groups = ['LSUP'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
        ]
    template_name = 'Guia.html'
    template_name = 'Form.html'
    form_class = DestaqueSupervisorForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.datatime = timezone.now()
            form.save()
            return HttpResponseRedirect(reverse('SupervisoresOficial'))
        else:
            return self.get(request, *args, **kwargs)
        
class PermissoesSupView(PatenteRequiredMixin, ListView):
    allowed_groups = ['RSUP', 'LSUP'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'Tenente-General ★★★',
            'Major-Brigadeiro ★★',
            'Brigadeiro-General ★',
        ]
    template_name = 'Guia.html'
    model = MilitarUsuario
    template_name = 'PermissoesSup.html'
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
            militar.is_sup = 'SUP' in [group.name for group in militar.groups.all()]
            militar.is_rsup = 'RSUP' in [group.name for group in militar.groups.all()]
            militar.is_lsup = 'LSUP' in [group.name for group in militar.groups.all()]

        context.update({
            'groups': grupos,
        })
        return context

@method_decorator(csrf_protect, name='dispatch')
class AdicionarSupView(PatenteRequiredMixin,View):
    allowed_groups = ['RSUP', 'LSUP'] 
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
        group = Group.objects.get(name='SUP')
        user.groups.add(group)
        return redirect('PermissõesSup')

@method_decorator(csrf_protect, name='dispatch')
class RemoverSupView(PatenteRequiredMixin,View):
    allowed_groups = ['RSUP', 'LSUP'] 
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
        group = Group.objects.get(name='SUP')
        user.groups.remove(group)
        return redirect('PermissõesSup')
    
@method_decorator(csrf_protect, name='dispatch')
class AdicionarRSupView(PatenteRequiredMixin,View):
    allowed_groups = ['LSUP'] 
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
        group = Group.objects.get(name='RSUP')
        user.groups.add(group)
        return redirect('PermissõesSup')

@method_decorator(csrf_protect, name='dispatch')
class RemoverRSupView(PatenteRequiredMixin,View):
    allowed_groups = ['LSUP'] 
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
        group = Group.objects.get(name='RSUP')
        user.groups.remove(group)
        return redirect('PermissõesSup')
    
@method_decorator(csrf_protect, name='dispatch')
class AdicionarLSupView(PatenteRequiredMixin,View):
    allowed_groups = ['LSUP'] 
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
        group = Group.objects.get(name='LSUP')
        user.groups.add(group)
        return redirect('PermissõesSup')

@method_decorator(csrf_protect, name='dispatch')
class RemoverLSupView(PatenteRequiredMixin,View):
    allowed_groups = ['LSUP'] 
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
        group = Group.objects.get(name='LSUP')
        user.groups.remove(group)
        return redirect('PermissõesSup')