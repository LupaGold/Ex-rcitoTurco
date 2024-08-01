from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import EmblemasModel, EmblemaCompra, MoedaValor, MoedaSaqueMoedaValor
from django.contrib import messages
from django.db import transaction
from django.views.generic import TemplateView, CreateView, UpdateView
from django.db.models import Count
from Militares.models import MilitarUsuario
from django.urls import reverse_lazy
from django.views.generic import ListView
from .forms import EmblemasForm
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ConAcs.views import PatenteRequiredMixin

User = get_user_model()

class LojaEmblemasView(PatenteRequiredMixin, TemplateView):
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
    template_name = 'Loja.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emblemas = EmblemasModel.objects.all().order_by('-datatime')
        emblemas_comprados = EmblemaCompra.objects.filter(solicitante=self.request.user).values_list('emblema_id', flat=True)
        context['emblemas'] = emblemas
        context['emblemas_comprados'] = emblemas_comprados
        context['total'] = EmblemasModel.objects.all().count()
        return context

class EditarEmblemas(PatenteRequiredMixin, ListView):
    allowed_groups = [] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    template_name = 'EditarEmblemas.html'
    context_object_name = 'emblemas'
    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = EmblemasModel.objects.all()

        if q:
            queryset = queryset.filter(titulo__icontains=q)

        return queryset.order_by('-datatime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = EmblemasModel.objects.all().count()
        return context

class EditarEmblemaView(PatenteRequiredMixin,UpdateView):
    allowed_groups = [] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    model = EmblemasModel
    form_class = EmblemasForm
    template_name = 'Form.html'
    success_url = reverse_lazy('EditarEmblemas') 

    def form_valid(self, form):
        emblema = form.save(commit=False)
        emblema.datatime = timezone.now() 
        emblema.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Editar emblema!'
        context["image"] = 'destaque.png'
        context["descricao"] = 'O tamanho do emblema deve ser de 40px por 40px!'
        return context

class RegistrarEmblema(PatenteRequiredMixin,CreateView):
    allowed_groups = [] 
    allowed_patentes = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]
    form_class = EmblemasForm
    template_name = 'Form.html'
    success_url = reverse_lazy('LojaEmblemas')

    def form_valid(self, form):
        emblema = form.save(commit=False)
        emblema.solicitante = self.request.user
        emblema.datatime = timezone.now()
        emblema.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar emblema!'
        context["image"] = 'destaque.png'
        context["descricao"] = 'O tamanho do emblema deve ser de 40px por 40px!'
        return context

class ComprarEmblemaView(PatenteRequiredMixin, View):
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
    def post(self, request, *args, **kwargs):
        emblema_id = kwargs.get('emblema_id')
        emblema = get_object_or_404(EmblemasModel, id=emblema_id)
        usuario = request.user

        # Verifica se o usuário já tem o emblema
        if EmblemaCompra.objects.filter(solicitante=usuario, emblema=emblema).exists():
            messages.error(request, 'Você já comprou este emblema.')
            return redirect(reverse('LojaEmblemas'))

        # Verifica se o usuário tem moedas
        if usuario.moedas < emblema.moedas:
            messages.error(request, 'Você não tem moedas suficientes para comprar este emblema.')
            return redirect(reverse('LojaEmblemas'))

        with transaction.atomic():
            # Deduz o coin do usuário
            usuario.moedas -= emblema.moedas
            usuario.save()

            # Cria a compra do emblema
            EmblemaCompra.objects.create(solicitante=usuario, emblema=emblema)

        messages.success(request, 'Emblema comprado com sucesso!')
        return redirect(reverse('LojaEmblemas'))

class MoedasMilitaresView(PatenteRequiredMixin, ListView):
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
    model = MilitarUsuario
    template_name = 'MoedasMilitares.html'
    context_object_name = 'militares'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = MilitarUsuario.objects.all()

        if q:
            queryset = queryset.filter(username__icontains=q)

        return queryset.order_by('-data')
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_moedas_url'] = reverse_lazy('AdicionarMoedas')
        context['remove_moedas_url'] = reverse_lazy('RemoverMoedas')
        return context

class AddMoedasView(PatenteRequiredMixin, View):
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
        user_id = request.POST.get('user_id')
        amount = request.POST.get('amount')

        if not amount or not amount.strip():
            messages.error(request, 'Por favor, insira uma quantidade válida de moedas.')
            return redirect('MoedasMilitares')

        try:
            amount = float(amount)
        except ValueError:
            messages.error(request, 'Por favor, insira uma quantidade válida de moedas.')
            return redirect('MoedasMilitares')

        user = get_object_or_404(MilitarUsuario, id=user_id)
        user.moedas += amount
        user.save()
        messages.success(request, f'{amount} moedas adicionadas a {user.username}.')
        return redirect('MoedasMilitares')

class RemoveMoedasView(PatenteRequiredMixin, View):
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
        user_id = request.POST.get('user_id')
        amount = request.POST.get('amount')

        if not amount or not amount.strip():
            messages.error(request, 'Por favor, insira uma quantidade válida de moedas.')
            return redirect('MoedasMilitares')

        try:
            amount = float(amount)
        except ValueError:
            messages.error(request, 'Por favor, insira uma quantidade válida de moedas.')
            return redirect('MoedasMilitares')

        user = get_object_or_404(MilitarUsuario, id=user_id)
        user.moedas -= amount
        if user.moedas < 0:
            user.moedas = 0
        user.save()
        messages.success(request, f'{amount} moedas removidas de {user.username}.')
        return redirect('MoedasMilitares')
    
class MoedasLoja(PatenteRequiredMixin, TemplateView):
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
    template_name = 'MoedasLoja.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['moedasvalor'] = MoedaValor.objects.all().order_by('-datatime')
        return context
    
class SaqueMoedas(PatenteRequiredMixin, View):
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
    def post(self, request, *args, **kwargs):
        moeda_id = kwargs.get('moeda_id')
        moeda = get_object_or_404(MoedaValor, id=moeda_id)
        usuario = request.user

        # Verifica se o usuário tem moedas
        if usuario.moedas < moeda.moedas:
            messages.error(request, 'Você não tem moedas suficientes para sacar esse valor.')
            return redirect(reverse('MoedasLoja'))

        with transaction.atomic():
            # Deduz o coin do usuário
            usuario.moedas -= moeda.moedas
            usuario.save()

            # Cria a compra do emblema
            MoedaSaqueMoedaValor.objects.create(solicitante=usuario, icone=moeda, status='Em processamento...', datatime=timezone.now())

        messages.success(request, 'Saque realizado com sucesso!')
        return redirect(reverse('MoedasLoja'))