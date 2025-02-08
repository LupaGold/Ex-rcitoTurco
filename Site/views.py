from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView
from SegundaCIA.models import Treinamentos
from Militares.models import MilitarUsuario
from django.contrib.auth.models import Group
from Jornal.models import PostagemJornal
from .models import PaginaSite
from Honrarias.models import HonrariaMilitar
from Militares.models import MilitarUsuario
from Loja.models import EmblemaCompra
from ConAcs.views import PatenteRequiredMixin
from Treinamentos.models import RelatoriosDeTreinamento
from Recrutamento.models import Re

#Viw da página principal do site
class SitePrincipal(TemplateView):
    template_name = 'Principal.html'

    def get(self, request, *args, **kwargs):
        search_term = request.GET.get('search', '')
        militar = MilitarUsuario.objects.filter(username__icontains=search_term) if search_term else None
        honrarias = HonrariaMilitar.objects.filter(militar__username__icontains=search_term)
        patentes = ['Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
            'Tenente-Coronel',
            'Major',
            'Capitão',
            'Primeiro Tenente',
            'Segundo Tenente',
            'Aspirante-a-Oficial']
        context = {
            'militar': militar,
            'noticias': PostagemJornal.objects.last(),
            'militares': MilitarUsuario.objects.filter(patente__in=patentes, status='Ativo'),
            'ultimosalistados': MilitarUsuario.objects.order_by('-id')[:4],
            'busca': search_term,
            'honrarias': honrarias,
        }
        return self.render_to_response(context)

class DemitidosSite(TemplateView):
    template_name = 'Demitidos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Mapeia as patentes para suas ordens correspondentes
            patente_order_map = {
                'Marechal ★★★★★': 1,
                'General-de-Exército ★★★★': 2,
                'General-de-Divisão ★★★': 3,
                'General-de-Brigada ★★': 4,
                'Coronel ★': 5,
                'Tenente-Coronel': 6,
                'Major': 7,
                'Capitão': 8,
                'Primeiro Tenente': 9,
                'Segundo Tenente': 10,
                'Aspirante-a-Oficial': 11,
                'Cadete': 12,
                'Subtenente': 13,
                'Primeiro Sargento': 14,
                'Segundo Sargento': 15,
                'Terceiro Sargento': 16,
                'Aluno': 17,
                'Cabo': 18,
                'Soldado Estrela': 19,
                'Soldado': 20,
            }

            # Recupera todas as patentes distintas dos usuários e as ordena usando patente_order_map
            patentes = sorted(patente_order_map, key=lambda x: patente_order_map[x])

            # Remova a patente "Marechal" da lista de patentes
            patentes_sem_marechal = [patente for patente in patentes if patente != 'Marechal ★★★★★']

            # Lista para armazenar as informações de usuários por patente
            usuarios_por_patente = []

            # Itera sobre cada patente
            for patente in patentes_sem_marechal:
                # Filtra os usuários por patente
                usuarios = MilitarUsuario.objects.filter(patente=patente, status="Demitido")
                # Adiciona os usuários formatados à lista
                usuarios_formatados = []
                for index, usuario in enumerate(usuarios, start=1):
                    usuarios_formatados.append(f"{index}- {usuario.username} - {usuario.patente} - {usuario.data} - {usuario.responsavel_promocao} - {usuario.demissao_motivo}")
                # Adiciona as informações da patente e usuários à lista
                usuarios_por_patente.append((patente, usuarios_formatados))

            context["demitidos"] = usuarios_por_patente
        except Exception as e:
            context["error"] = str(e)
        return context

#View da listagem de Praças e Oficiais
class PraçasEOficiais(TemplateView):
    template_name = 'PraçasEOficiais.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Mapeia as patentes para suas ordens correspondentes
            patente_order_map = {
                'Marechal ★★★★★': 1,
                'General-de-Exército ★★★★': 2,
                'General-de-Divisão ★★★': 3,
                'General-de-Brigada ★★': 4,
                'Coronel ★': 5,
                'Tenente-Coronel': 6,
                'Major': 7,
                'Capitão': 8,
                'Primeiro Tenente': 9,
                'Segundo Tenente': 10,
                'Aspirante-a-Oficial': 11,
                'Cadete': 12,
                'Subtenente': 13,
                'Primeiro Sargento': 14,
                'Segundo Sargento': 15,
                'Terceiro Sargento': 16,
                'Aluno': 17,
                'Cabo': 18,
                'Soldado Estrela': 19,
                'Soldado': 20,
            }

            # Recupera todas as patentes distintas dos usuários e as ordena usando patente_order_map
            patentes = sorted(patente_order_map, key=lambda x: patente_order_map[x])


            # Lista para armazenar as informações de usuários por patente
            usuarios_por_patente = []

            # Itera sobre cada patente
            for patente in patentes:
                # Filtra os usuários por patente
                usuarios = MilitarUsuario.objects.filter(patente=patente, status="Ativo")
                # Adiciona os usuários formatados à lista
                usuarios_formatados = []
                for index, usuario in enumerate(usuarios, start=1):
                    usuarios_formatados.append(f"{index}- {usuario.username} - {usuario.patente} - {usuario.data} - {usuario.responsavel_promocao} ")
                # Adiciona as informações da patente e usuários à lista
                usuarios_por_patente.append((patente, usuarios_formatados))

            context["praçaseoficiais"] = usuarios_por_patente
        except Exception as e:
            context["error"] = str(e)
        return context

#View do site da 2CIA
class SegundaCIA(TemplateView):
    model = Treinamentos
    template_name = 'SegundaCompanhia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Grupos Líder e Membro da 2CIA
        lider = 'L2CIA'
        membro = 'M2CIA'
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

        context['treinamentos'] = Treinamentos.objects.all().order_by('datatime')
        return context

#View de aposentados
class AposentadosSite(TemplateView):
    template_name = "Aposentados.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["aposentados"] = MilitarUsuario.objects.filter(status='Aposentado').order_by('patente_order','-data')
        context["ultimosalistados"] = MilitarUsuario.objects.order_by('-id')[:5]
        return context

#View para ver as páginas individualmente
class PaginasLoad(DetailView):
    model = PaginaSite
    template_name = 'PaginasSite.html'
    context_object_name = 'item'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ultimosalistados"] = MilitarUsuario.objects.order_by('-id')[:5]
        return context

#View para ver o perfil do militar
class PerfilMilitar(DetailView):
    model = MilitarUsuario
    template_name = 'PerfilMilitar.html'
    context_object_name = 'perfil'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtenha o objeto MilitarUsuario atual
        militar = self.get_object()
        # Obtenha os emblemas comprados pelo militar
        emblemas_comprados = EmblemaCompra.objects.filter(solicitante=militar)
        # Adicione os emblemas ao contexto
        context['treinamentos'] = RelatoriosDeTreinamento.objects.filter(treinador=militar.username).count()
        context['re'] = Re.objects.filter(militar=militar.username).count
        context['emblemas'] = emblemas_comprados
        context["ultimosalistados"] = MilitarUsuario.objects.order_by('-id')[:5]
        return context

class RegimentoSite(TemplateView):
    template_name = "Regimento.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ultimosalistados"] = MilitarUsuario.objects.order_by('-id')[:5]
        return context