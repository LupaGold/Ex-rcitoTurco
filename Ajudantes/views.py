from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView, UpdateView
from .models import AjudanteRelatorio, GuiaAjudantes, DestaqueAjudantes
from django.db.models import Count
from .forms import GuiaAjudanteForm, AjudanteForm, DestaqueAjudanteForm
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

class AjudantePraça(PatenteRequiredMixin,TemplateView):
    allowed_groups = ['AJD', 'RAJD', 'LAJD'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    model = AjudanteRelatorio
    template_name = 'AjudantesPraças.html'

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

        context['relatorios'] = AjudanteRelatorio.objects.filter(solicitante=self.request.user).order_by('-data')
        context['contador'] = AjudanteRelatorio.objects.filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        ).values('palestra').annotate(total=Count('palestra'))
        context['total'] = AjudanteRelatorio.objects.filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        ).count()
        # Agregação dos dados para contar o número de palestras enviadas por cada treinador
        ranking = (
            AjudanteRelatorio.objects
            .filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        )
            .values('treinador')
            .annotate(total_palestras=Count('id'))
            .order_by('-total_palestras')
        )

        # Convertemos o QuerySet para uma lista de dicionários
        context['destaque'] = DestaqueAjudantes.objects.last()
        context['ranking'] = ranking
        context['dias_falta'] = dias_falta
        context['horas_falta'] = horas_falta
        context['minutos_falta'] = minutos_falta
        context['segundos_falta'] = segundos_falta


        return context

class RegistrarRelatorioAjudante(PatenteRequiredMixin,CreateView):
    allowed_groups = ['AJD', 'RAJD', 'LAJD'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    form_class = AjudanteForm
    template_name = 'Form.html'
    success_url = reverse_lazy('AjudantesPraça')

    
    def form_valid(self, form):
        sup = form.save(commit=False)
        sup.solicitante = self.request.user
        sup.data = timezone.now()
        sup.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar ação de Helper!'
        context["image"] = 'ajudantes.gif'
        context["descricao"] = 'Verifique todos os campos antes de enviar o relatório!'
        return context
    
# class SupSite(TemplateView):
#     model = PalestraSupervisores
#     template_name = 'SupervisoresPalestras.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         #Grupos Líder e Membro da 2CIA
#         lider = 'LSUP'  
#         membro = 'RSUP'
#         #Lógica para testar os Militares se fazem parte dos grupos
#         try:
#             grupo_lider = Group.objects.get(name=lider)
#             context['lider'] = MilitarUsuario.objects.filter(groups=grupo_lider).first()
#         except Group.DoesNotExist:
#             context['lider'] = MilitarUsuario.objects.none()
        
#         try:
#             grupo_membro = Group.objects.get(name=membro)
#             context['membros'] = MilitarUsuario.objects.filter(groups=grupo_membro).order_by('patente_order')
#         except Group.DoesNotExist:
#             context['membros'] = MilitarUsuario.objects.none()

#         context['treinamentos'] = PalestraSupervisores.objects.all()
#         return context

class AjudanteOficial(PatenteRequiredMixin,ListView):
    allowed_groups = ['RAJD', 'LAJD'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    model = AjudanteRelatorio
    template_name = 'AjudantesOficiais.html'
    context_object_name = 'relatorios'

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = AjudanteRelatorio.objects.all()

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

        context['contador'] = AjudanteRelatorio.objects.filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        ).values('palestra').annotate(total=Count('palestra'))
        context['total'] = AjudanteRelatorio.objects.filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        ).count()
        # Agregação dos dados para contar o número de palestras enviadas por cada treinador
        ranking = (
            AjudanteRelatorio.objects
            .filter(
            data__gte=ultima_segunda,
            data__lt=proxima_segunda
        )
            .values('treinador')
            .annotate(total_palestras=Count('id'))
            .order_by('-total_palestras')
        )

        # Convertemos o QuerySet para uma lista de dicionários
        context['destaque'] = DestaqueAjudantes.objects.last()
        context['ranking'] = ranking
        context['dias_falta'] = dias_falta
        context['horas_falta'] = horas_falta
        context['minutos_falta'] = minutos_falta
        context['segundos_falta'] = segundos_falta
        return context
    
# class PalestraSupervisoresUpdateView(UpdateView):
#     model = PalestraSupervisores
#     form_class = PalestraSupervisoresForm
#     template_name = 'Form.html'
#     success_url = reverse_lazy('SupSite')

class GuiaAjudantesEdit(PatenteRequiredMixin,UpdateView):
    allowed_groups = ['RAJD', 'LAJD'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    model = GuiaAjudantes
    form_class = GuiaAjudanteForm
    template_name = 'Form.html'
    success_url = reverse_lazy('GuiaAjudantes')

class GuiaAjudantesView(PatenteRequiredMixin,TemplateView):
    allowed_groups = ['AJD', 'RAJD', 'LAJD'] 
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
        context["guia"] = GuiaAjudantes.objects.last()
        return context
    
class CriarDestaqueAjd(PatenteRequiredMixin,CreateView):
    allowed_groups = ['LAJD'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    template_name = 'Form.html'
    form_class = DestaqueAjudanteForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.data = timezone.now()
            form.save()
            return HttpResponseRedirect(reverse('AjudantesOficial'))
        else:
            return self.get(request, *args, **kwargs)
        
class PermissoesAjdView(PatenteRequiredMixin ,ListView):
    allowed_groups = ['RAJD', 'LAJD'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    model = MilitarUsuario
    template_name = 'PermissoesAjd.html'
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
            militar.is_sup = 'AJD' in [group.name for group in militar.groups.all()]
            militar.is_rsup = 'RAJD' in [group.name for group in militar.groups.all()]
            militar.is_lsup = 'LAJD' in [group.name for group in militar.groups.all()]

        context.update({
            'groups': grupos,
        })
        return context

@method_decorator(csrf_protect, name='dispatch')
class AdicionarAjdView(PatenteRequiredMixin,View):
    allowed_groups = ['RAJD', 'LAJD'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        group = Group.objects.get(name='AJD')
        user.groups.add(group)
        return redirect('PermissoesAjd')

@method_decorator(csrf_protect, name='dispatch')
class RemoverAjdView(PatenteRequiredMixin,View):
    allowed_groups = ['RAJD', 'LAJD'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        group = Group.objects.get(name='AJD')
        user.groups.remove(group)
        return redirect('PermissoesAjd')
    
@method_decorator(csrf_protect, name='dispatch')
class AdicionarRAjdView(PatenteRequiredMixin,View):
    allowed_groups = ['LAJD'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        group = Group.objects.get(name='RAJD')
        user.groups.add(group)
        return redirect('PermissoesAjd')

@method_decorator(csrf_protect, name='dispatch')
class RemoverRAjdView(PatenteRequiredMixin,View):
    allowed_groups = ['LAJD'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        group = Group.objects.get(name='RAJD')
        user.groups.remove(group)
        return redirect('PermissoesAjd')
    
@method_decorator(csrf_protect, name='dispatch')
class AdicionarLAjdView(PatenteRequiredMixin,View):
    allowed_groups = ['LAJD'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        group = Group.objects.get(name='LAJD')
        user.groups.add(group)
        return redirect('PermissoesAjd')

@method_decorator(csrf_protect, name='dispatch')
class RemoverLAjdView(PatenteRequiredMixin,View):
    allowed_groups = ['LAJD'] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        group = Group.objects.get(name='LAJD')
        user.groups.remove(group)
        return redirect('PermissoesAjd')