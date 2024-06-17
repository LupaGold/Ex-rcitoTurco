from django.shortcuts import render
from ConAcs.views import PatenteRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView
from .models import Re, LogRE 
from .forms import ReForm
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect

# View de relatórios
User = get_user_model()

class RePraça(PatenteRequiredMixin,TemplateView):
    allowed_groups = [] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    model = Re
    template_name = 'RePraça.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recrutamentos'] = Re.objects.filter(solicitante=self.request.user).order_by('-abertura')
        return context

class AbrirRE(PatenteRequiredMixin,CreateView):
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
            form.instance.abertura = timezone.now()
            relatorio = form.save()

            # Incrementar moedas do solicitante
            solicitante = relatorio.solicitante
            solicitante.moedas += 1
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
                        "message": f"Atenção um Recrutamento Externo foi aberto por {relatorio.solicitante.username} às."
                    }
                )
            log = LogRE.objects.create(
                    re=relatorio,
                    texto=f"{relatorio.solicitante} enviou abriu um Recrutamento Externo!",
                    datatime=timezone.now(),
                )

            log.save()

            return HttpResponseRedirect(reverse('RePraça'))
        else:
            return self.get(request, *args, **kwargs)