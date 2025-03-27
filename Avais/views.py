from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView
from .models import JA, LogJA
from .forms import JAForm
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from ConAcs.views import PatenteRequiredMixin
from django.db.models import Count

# View de Aval de Praças
User = get_user_model()

class AvalPraça(PatenteRequiredMixin,TemplateView):
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
    model = JA
    template_name = 'AvaisPraças.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avais'] = JA.objects.filter(solicitante=self.request.user).order_by('-datatime')
        return context

class RegistrarAval(PatenteRequiredMixin,CreateView):
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
    form_class = JAForm
    template_name = 'Form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar Aval'
        context["image"] = 'relatorio.png'
        context["descricao"] = 'Verifique todos os campos antes de registrar o Aval!'
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.solicitante = self.request.user
            new_ja = form.save()
            
            log = LogJA.objects.create(
                    aval=new_ja,
                    texto=f"{new_ja.solicitante} enviou um aval!",
                    datatime=timezone.now(),
                )

            log.save()

            return HttpResponseRedirect(reverse('AvalPraça'))
        else:
            return self.get(request, *args, **kwargs)
        
class AvalAC(PatenteRequiredMixin, ListView):
    allowed_groups = [] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
            'Tenente-Coronel',
            'Major',
        ]
    model = JA
    template_name = 'AvaisAC.html'
    context_object_name = 'avais'

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = JA.objects.all()

        if q:
            queryset = queryset.filter(solicitante__username__icontains=q)
            print('passou')
            print(q)

        queryset = queryset.order_by('-datatime')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = JA.objects.all().count()
        return context
    
class AprovarJAView(PatenteRequiredMixin, View):
    allowed_groups = [] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
            'Tenente-Coronel',
            'Major',
        ]
    def post(self, request, *args, **kwargs):
        ja_id = kwargs.get('ja_id')
        ja = get_object_or_404(JA, id=ja_id)
        ja.status = 'Aprovado'
        ja.save()

        LogJA.objects.create(
            aval=ja,
            texto=f'O JA solicitado por {ja.solicitante.patente} {ja.solicitante.username} foi aprovado por {request.user.username}.',
            datatime=timezone.now()
        )
        

        return HttpResponseRedirect(reverse('AvalAC'))

class RejeitarJAView(PatenteRequiredMixin, View):
    allowed_groups = [] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
            'Tenente-Coronel',
            'Major',
        ]
    def post(self, request, *args, **kwargs):
        ja_id = kwargs.get('ja_id')
        ja = get_object_or_404(JA, id=ja_id)
        ja.status = 'Reprovado'
        ja.save()

        LogJA.objects.create(
            aval=ja,
            texto=f'O JA solicitado por {ja.solicitante.patente} {ja.solicitante.username} foi rejeitado por {request.user.username}.',
            datatime=timezone.now()
        )

        return HttpResponseRedirect(reverse('AvalAC'))