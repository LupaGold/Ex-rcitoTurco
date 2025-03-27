import requests
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from Militares.models import MilitarUsuario
from .forms import CustomPasswordChangeForm, MilitarUsuarioCreationForm, CadastroForm
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView
from django.db.models import Count
from datetime import date
from django.forms import ModelForm
from django import forms
from django.views.generic.edit import UpdateView
from .forms import DestaqueOficialForm, DestaquePraçaForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
import random
import string

PATENTES = (
    ('', 'Selecione a Patente'),
    ('Soldado', 'Soldado'),
    ('Soldado de 1ª Classe', 'Soldado de 1ª Classe'),
    ('Especialista', 'Especialista'),
    ('Cabo', 'Cabo'),
    ('Aluno', 'Aluno'),
    ('Sargento', 'Sargento'),
    ('Sargento Staff', 'Sargento Staff'),
    ('Sargento Mestre', 'Sargento Mestre'),
    ('Sargento Major', 'Sargento Major'),
    ('Cadete', 'Cadete'),
    ('Aspirante-a-Oficial', 'Aspirante-a-Oficial'),
    ('Segundo Tenente', 'Segundo Tenente'),
    ('Primeiro Tenente', 'Primeiro Tenente'),
    ('Capitão', 'Capitão'),
    ('Major', 'Major'),
    ('Tenente-Coronel', 'Tenente-Coronel'),
    ('Coronel', 'Coronel'),
    ('Brigadeiro-General ★', 'Brigadeiro-General ★'),
    ('Major-General ★★', 'Major-General ★★'),
    ('Tenente-General ★★★', 'Tenente-General ★★★'),
    ('General-de-Exército ★★★★', 'General-de-Exército ★★★★'),
    ('Marechal ★★★★★', 'Marechal ★★★★★'),
)

# Mapeamento de patente atual para próxima patente
PROMOCAO = {
    'Soldado': 'Soldado de 1ª Classe',
    'Soldado de 1ª Classe': 'Cabo',
    'Cabo': 'Aluno',
    'Aluno': 'Sargento',
    'Sargento': 'Sargento Staff',
    'Sargento Staff': 'Sargento Mestre',
    'Sargento Mestre': 'Sargento Major',
    'Sargento Major': 'Cadete',
    'Cadete': 'Aspirante-a-Oficial',
    'Aspirante-a-Oficial': 'Segundo Tenente',
    'Segundo Tenente': 'Primeiro Tenente',
    'Primeiro Tenente': 'Capitão',
    'Capitão': 'Major',
    'Major': 'Tenente-Coronel',
    'Tenente-Coronel': 'Coronel',
    'Coronel': 'Brigadeiro-General ★',
    'Brigadeiro-General ★': 'Major-General ★★',
    'Major-General ★★': 'Tenente-General ★★★',
    'Tenente-General ★★★': 'General-de-Exército ★★★★',
    'General-de-Exército ★★★★': 'Marechal ★★★★★',
}

# Limites de promoção com base na patente do solicitante
LIMITES_PROMOCAO = {
    'Segundo Tenente': 'Sargento',
    'Primeiro Tenente': 'Sargento Staff',
    'Capitão': 'Sargento Staff',
    'Major': 'Sargento Mestre',
    'Tenente-Coronel': 'Sargento Major',
    'Coronel': 'Sargento Major',
    'Brigadeiro-General ★': 'Primeiro Tenente',
    'Major-General ★★': 'Capitão',
    'Tenente-General ★★★': 'Major',
    'General-de-Exército ★★★★': 'Tenente-Coronel',
    'Marechal ★★★★★': 'General-de-Exército ★★★★',
}

LIMITES_REBAIXAMENTO = {
    'Segundo Tenente': 'Sargento',
    'Primeiro Tenente': 'Sargento Staff',
    'Capitão': 'Sargento Mestre',
    'Major': 'Sargento Major',
    'Tenente-Coronel': 'Cadete',
    'Coronel': 'Cadete',
    'Brigadeiro-General ★': 'Capitão',
    'Major-General ★★': 'Major',
    'Tenente-General ★★★': 'Tenente-Coronel',
    'General-de-Exército ★★★★': 'Brigadeiro-General ★',
    'Marechal ★★★★★': 'Marechal ★★★★★',
}

LIMITES_DEMISSAO = {
    'Segundo Tenente': ['Soldado', 'Soldado de 1ª Classe', 'Especialista','Cabo', 'Aluno'],
    'Primeiro Tenente': ['Soldado', 'Soldado de 1ª Classe', 'Especialista','Cabo', 'Aluno', 'Sargento'],
    'Capitão': ['Soldado', 'Soldado de 1ª Classe', 'Especialista','Cabo', 'Aluno', 'Sargento', 'Sargento Staff'],
    'Major': ['Soldado', 'Soldado de 1ª Classe', 'Especialista','Cabo', 'Aluno', 'Sargento', 'Sargento Staff', 'Sargento Mestre'],
    'Tenente-Coronel': ['Soldado', 'Soldado de 1ª Classe', 'Cabo', 'Aluno', 'Sargento', 'Sargento Staff', 'Sargento Mestre', 'Sargento Major'],
    'Coronel': ['Soldado', 'Soldado de 1ª Classe', 'Especialista','Cabo', 'Aluno', 'Sargento', 'Sargento Staff', 'Sargento Mestre'],
    'Brigadeiro-General ★': ['Soldado', 'Soldado de 1ª Classe', 'Especialista','Cabo', 'Aluno', 'Sargento', 'Sargento Staff', 'Sargento Mestre', 'Sargento Major', 'Cadete','Aspirante-a-Oficial', 'Segundo Tenente', 'Primeiro Tenente'],
    'Major-General ★★': ['Soldado', 'Soldado de 1ª Classe', 'Especialista','Cabo', 'Aluno', 'Sargento', 'Sargento Staff', 'Sargento Mestre', 'Sargento Major', 'Cadete','Aspirante-a-Oficial', 'Segundo Tenente', 'Primeiro Tenente', 'Capitão', 'Major'],
    'Tenente-General ★★★': ['Soldado', 'Soldado de 1ª Classe', 'Especialista','Cabo', 'Aluno', 'Sargento', 'Sargento Staff', 'Sargento Mestre', 'Sargento Major', 'Cadete','Aspirante-a-Oficial', 'Segundo Tenente', 'Primeiro Tenente', 'Capitão', 'Major', 'Tenente-Coronel'],
    'General-de-Exército ★★★★': ['Soldado', 'Soldado de 1ª Classe', 'Especialista','Cabo', 'Aluno', 'Sargento', 'Sargento Staff', 'Sargento Mestre', 'Sargento Major', 'Cadete','Aspirante-a-Oficial', 'Segundo Tenente', 'Primeiro Tenente', 'Capitão', 'Major', 'Tenente-Coronel', 'Brigadeiro-General ★'],
    'Marechal ★★★★★': ['Soldado', 'Soldado de 1ª Classe', 'Especialista','Cabo', 'Aluno', 'Sargento', 'Sargento Staff', 'Sargento Mestre', 'Sargento Major', 'Cadete','Aspirante-a-Oficial', 'Segundo Tenente', 'Primeiro Tenente', 'Capitão', 'Major', 'Tenente-Coronel', 'Brigadeiro-General ★', 'Major-General ★★', 'Tenente-General ★★★', 'General-de-Exército ★★★★'],
}

PATENTES_APOSENTADORIA = [
    'Capitão', 'Major', 'Tenente-Coronel', 'Coronel','Brigadeiro-General ★',
    'Major-General ★★', 'Tenente-General ★★★',
    'General-de-Exército ★★★★', 'Marechal ★★★★★'
]

class PatenteRequiredMixin(LoginRequiredMixin):
    allowed_groups = []  # Defina os grupos permitidos
    allowed_patentes = []  # Defina as patentes permitidas
    login_url = reverse_lazy('LoginPainel')  # URL da página de login

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Se o usuário não estiver autenticado, redirecione para a página de login
            return self.handle_no_permission()

        user = request.user

        # Verifica se o usuário pertence a algum grupo permitido
        is_in_allowed_group = False
        if self.allowed_groups:
            is_in_allowed_group = any(group in self.allowed_groups for group in user.groups.values_list('name', flat=True))

        # Verifica se a patente do usuário está na lista de patentes permitidas
        is_patente_allowed = user.patente in self.allowed_patentes

        # Se o usuário não estiver em nenhum grupo permitido e sua patente não estiver na lista permitida
        if not is_in_allowed_group and not is_patente_allowed:
            # Renderiza página de erro de permissão
            return render(request, 'ErroPermissão.html')

        # Se passou nas validações, continua com o dispatch padrão
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        # Sobrescreve o método handle_no_permission para redirecionar para a página de login
        return super().handle_no_permission()

class LoginViewModificada(LoginView):
    template_name = 'Login.html'
    authentication_form = LoginForm

class AlterarSenhaView(PatenteRequiredMixin, PasswordChangeView):
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
    template_name = 'Form.html'
    success_url = reverse_lazy('AlterarSenha')
    form_class = CustomPasswordChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players_data'] =  MilitarUsuario.objects.filter(username=self.request.user)
        context["titulo"] = 'Alterar Senha'
        context["image"] = 'cadeado.gif'
        context["descricao"] = 'Uma senha segura evita acessos indesejados em sua conta!'
        return context

class MilitaresLista(ListView):
    model = MilitarUsuario
    template_name = 'MilitaresLista.html'
    context_object_name = 'militares'
    paginate_by = 20
    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = MilitarUsuario.objects.all()

        if q:
            queryset = queryset.filter(username__icontains=q)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contador'] = MilitarUsuario.objects.count()
        return context

class PromoverUsuarioView(LoginRequiredMixin, View):
    @method_decorator(csrf_protect)
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        solicitante = request.user

        # Verificar a patente do solicitante
        solicitante_patente = solicitante.patente
        limite_patente = LIMITES_PROMOCAO.get(solicitante_patente)

        if not limite_patente:
            messages.error(request, 'Você não tem permissão para promover usuários.')
            return redirect('MilitaresLista')

        # Verificar a próxima patente do usuário
        patente_atual = user.patente
        proxima_patente = PROMOCAO.get(patente_atual)

        if not proxima_patente:
            messages.error(request, 'Não foi possível promover o usuário.')
            return redirect('MilitaresLista')

        # Verificar se a promoção está dentro do limite
        patentes_ordenadas = [patente[0] for patente in PATENTES]
        indice_limite = patentes_ordenadas.index(limite_patente)
        indice_proxima = patentes_ordenadas.index(proxima_patente)

        if indice_proxima > indice_limite:
            messages.error(request, 'Você não tem permissão para promover o usuário para essa patente.')
            return redirect('MilitaresLista')

        # Promover o usuário
        user.patente = proxima_patente
        user.data = date.today()
        user.responsavel_promocao = request.user.username
        user.save()
        messages.success(request, f'Usuário {user.username} promovido para {proxima_patente}.')
        return redirect('MilitaresLista')

class RebaixarUsuarioView(LoginRequiredMixin, View):
    @method_decorator(csrf_protect)
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        solicitante = request.user

        # Verificar a patente do solicitante
        solicitante_patente = solicitante.patente
        limite_patente = LIMITES_REBAIXAMENTO.get(solicitante_patente)

        if not limite_patente:
            messages.error(request, 'Você não tem permissão para rebaixar usuários.')
            return redirect('MilitaresLista')

        # Verificar a patente atual do usuário
        patente_atual = user.patente
        patentes_ordenadas = [patente[0] for patente in PATENTES]

        if patente_atual not in patentes_ordenadas:
            messages.error(request, 'Não foi possível rebaixar o usuário.')
            return redirect('MilitaresLista')

        indice_atual = patentes_ordenadas.index(patente_atual)
        indice_limite = patentes_ordenadas.index(limite_patente)

        if indice_atual >= indice_limite:
            messages.error(request, 'Você não tem permissão para rebaixar o usuário para essa patente.')
            return redirect('MilitaresLista')

        # Rebaixar o usuário para a patente anterior
        proxima_patente = patentes_ordenadas[indice_atual - 1]
        user.patente = proxima_patente
        user.data = date.today()  # Registrar a data de rebaixamento
        user.responsavel_promocao = request.user.username  # Registrar o responsável pelo rebaixamento
        user.save()
        messages.success(request, f'Usuário {user.username} rebaixado para {proxima_patente}.')
        return redirect('MilitaresLista')

@method_decorator(csrf_protect, name='dispatch')
class AlterarStatusView(View):
    def post(self, request, user_id, status):
        user = get_object_or_404(MilitarUsuario, id=user_id)

        if status == 'Aposentado' and user.patente not in PATENTES_APOSENTADORIA:
            messages.error(request, "Apenas usuários com patente de Capitão ou superior podem se aposentar.")
            return redirect('MilitaresLista')

        if request.user.patente != 'Marechal ★★★★★':
            messages.error(request, "Apenas Marechais podem alterar o status de outros usuários.")
            return redirect('MilitaresLista')

        user.status = status
        if status == 'Aposentado':
            user.data = date.today()
            user.responsavel_promocao = request.user.username
        user.save()
        return redirect('MilitaresLista')

class DemitirMilitarView(View):
    @method_decorator(csrf_protect)
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)

        if not self.user_tem_permissao(request.user, user):
            messages.error(request, "Você não tem permissão para demitir este usuário.")
            return redirect('MilitaresLista')  # Substitua pelo nome da sua URL de lista de militares

        user.status = 'Demitido'
        user.data = date.today()
        user.responsavel_promocao = request.user.username
        user.save()
        messages.success(request, f"{user.username} foi demitido com sucesso.")
        return redirect('MilitaresLista')  # Substitua pelo nome da sua URL de lista de militares

    def user_tem_permissao(self, request_user, user):
        if not request_user.patente:
            return False

        # Verificar se o usuário tem uma patente que permite rebaixar outros usuários
        limites_rebaixamento = LIMITES_DEMISSAO.get(request_user.patente, [])
        return user.patente in limites_rebaixamento

class RegistroUsuarioView(CreateView):
    model = MilitarUsuario
    form_class = MilitarUsuarioCreationForm
    template_name = 'Form.html'
    success_url = reverse_lazy('MilitaresLista')  # Redireciona para a página de login após o registro

    def form_valid(self, form):
        senha_padrao = 'padrão$!%#!#¨!#al14912948242'  # Aqui você define sua senha padrão

        # Configurar o usuário com senha padrão
        user = form.save(commit=False)
        user.set_password(senha_padrao)

        # Setar o responsável pela promoção e a data atual
        user.responsavel_promocao = self.request.user.username
        user.data = date.today()

        messages.success(self.request, 'Usuário registrado com sucesso.')
        return super().form_valid(form)

class CriarDestaquePraça(CreateView):
    template_name = 'Form.html'
    form_class = DestaquePraçaForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.datatime = timezone.now()
            form.save()
            messages.success(request, "Praça destaque alterado com sucesso!")
            return HttpResponseRedirect(reverse('MilitaresLista'))
        else:
            return self.get(request, *args, **kwargs)

class CriarDestaqueOficial(CreateView):
    template_name = 'Form.html'
    form_class = DestaqueOficialForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.datatime = timezone.now()
            form.save()
            messages.success(request, "Oficial destaque alterado com sucesso!")
            return HttpResponseRedirect(reverse('MilitaresLista'))
        else:
            return self.get(request, *args, **kwargs)

class ResetarSenha(LoginRequiredMixin, View):
    @method_decorator(csrf_protect)
    def post(self, request, user_id):
        user = get_object_or_404(MilitarUsuario, id=user_id)
        solicitante = request.user

        # Verificar a patente do solicitante
        solicitante_patente = solicitante.patente
        limite_patente = LIMITES_REBAIXAMENTO.get(solicitante_patente)

        if not limite_patente:
            messages.error(request, 'Você não tem permissão para resetar a senha desse usuários.')
            return redirect('MilitaresLista')

        # Verificar a patente atual do usuário
        patente_atual = user.patente
        patentes_ordenadas = [patente[0] for patente in PATENTES]

        if patente_atual not in patentes_ordenadas:
            messages.error(request, 'Não foi possível resetar a senha do usuário.')
            return redirect('MilitaresLista')

        indice_atual = patentes_ordenadas.index(patente_atual)
        indice_limite = patentes_ordenadas.index(limite_patente)

        if indice_atual >= indice_limite:
            messages.error(request, 'Você não tem permissão para resetar a senha desse usuário.')
            return redirect('MilitaresLista')
        senha = self.GerarCódigo()
        # Rebaixar o usuário para a patente anterior
        user.set_password(senha)
        user.save()
        messages.success(request, f'Usuário {user.username} teve sua senha resetada para {senha}.')
        return redirect('MilitaresLista')
    
    def GerarCódigo(self):
        letters = string.ascii_uppercase
        digits = ''.join(random.choice(string.digits) for _ in range(4))
        return 'USA' + digits + 'SEC'
    
class PasswordView(TemplateView):
    template_name = 'change_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        codigo_aleatorio = self.GerarCódigo()
        context['form'] = CadastroForm()
        context['codigo_aleatorio'] = codigo_aleatorio
        return context

    def get(self, request):
        codigo_aleatorio = self.GerarCódigo()
        request.session['codigo_aleatorio'] = codigo_aleatorio
        form = CadastroForm(initial={'codigo_aleatorio': codigo_aleatorio})
        return render(request, self.template_name, {'form': form, 'codigo_aleatorio': codigo_aleatorio})

    def post(self, request, *args, **kwargs):
        form = CadastroForm(request.POST)
        codigo_aleatorio = request.session.get('codigo_aleatorio')
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if not self.CheckarUsuario(username):
                form.add_error(None, 'Policial não registrado!')
            elif self.CheckarCódigo(username, codigo_aleatorio):
                self.AlterarSenha(username, password)
                return redirect('login_principal')
            else:
                form.add_error(None, 'Código aleatório inválido')
        return render(request, self.template_name, {'form': form, 'codigo_aleatorio': codigo_aleatorio})


    def GerarCódigo(self):
        letters = string.ascii_uppercase
        digits = ''.join(random.choice(string.digits) for _ in range(3))
        return 'USA' + digits

    def CheckarUsuario(self, username):
        return MilitarUsuario.objects.filter(username__iexact=username).exists()

    def CheckarCódigo(self, username, codigo_aleatorio):
        try:
            response = requests.get(f'https://www.habbo.com.br/api/public/users?name={username}')
            if response.status_code == 200:
                data = response.json()
                motto = data.get('motto').strip()
                if codigo_aleatorio == motto:
                    return True
                else:
                    return False
            else:
                print(f"Erro na API: Status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a API: {e}")
            return False

    def AlterarSenha(self, username, password):
        user = MilitarUsuario.objects.get(username__iexact=username)
        user.set_password(password)
        user.save()