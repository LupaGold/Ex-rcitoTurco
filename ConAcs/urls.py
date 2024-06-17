from django.contrib import admin
from django.urls import path
from .views import (LoginViewModificada, AlterarSenhaView, MilitaresLista, PromoverUsuarioView, 
                    RebaixarUsuarioView, AlterarStatusView, DemitirMilitarView,RegistroUsuarioView,
                    CriarDestaqueOficial, CriarDestaquePraça, ResetarSenha)
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect(reverse_lazy('LoginPainel'))

urlpatterns = [
    path('login/', LoginViewModificada.as_view(), name='LoginPainel'),
    path('logout/', custom_logout, name ='Logout'),
    path('painel/alterar-senha/', AlterarSenhaView.as_view(), name='AlterarSenha'),
    path('painel/militares-lista//alterar-senha/<int:user_id>/', ResetarSenha.as_view(), name='ResetarSenha'),
    path('painel/militares-lista/', MilitaresLista.as_view(), name='MilitaresLista'),
    path('painel/militares-lista/criar-destaque-praça/', CriarDestaquePraça.as_view(), name='CriarDestaquePraça'),
    path('painel/militares-lista/criar-destaque-oficial/', CriarDestaqueOficial.as_view(), name='CriarDestaqueOficial'),
    path('painel/militares-lista/registrar/', RegistroUsuarioView.as_view(), name='RegistrarMilitar'),
    path('painel/militares-lista/promover/<int:user_id>/', PromoverUsuarioView.as_view(), name='PromoverMilitar'),
    path('painel/militares-lista/rebaixar/<int:user_id>/', RebaixarUsuarioView.as_view(), name='RebaixarMilitar'),
    path('painel/militares-lista/<int:user_id>/<str:status>/', AlterarStatusView.as_view(), name='AlterarStatus'),
    path('painel/militares-lista/demitir/<int:user_id>/', DemitirMilitarView.as_view(), name='DemitirMilitar')
]