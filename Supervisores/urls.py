from django.urls import path
from .views import (SupervisoresPraça, RegistrarRelatorioSupervisor, SupSite, SupervisoresOficial,
                    PalestraSupervisoresUpdateView, CriarDestaque, GuiaSupervisoresView, GuiaSupervisoresEdit
                    , PermissoesSupView, AdicionarSupView, RemoverSupView, AdicionarLSupView, AdicionarRSupView,
                    RemoverLSupView, RemoverRSupView)

urlpatterns = [
    path('supervisores-ações/', SupervisoresPraça.as_view(), name='SupervisoresPraça'),
    path('supervisores-guia/', GuiaSupervisoresView.as_view(), name='GuiaSupervisores'),
    path('supervisores-permissões/', PermissoesSupView.as_view(), name='PermissõesSup'),
    path('adicionar-sup/<int:user_id>/', AdicionarSupView.as_view(), name='AdicionarSup'),
    path('remover-sup/<int:user_id>/', RemoverSupView.as_view(), name='RemoverSup'),
    path('adicionar-rsup/<int:user_id>/', AdicionarRSupView.as_view(), name='AdicionarRSup'),
    path('remover-rsup/<int:user_id>/', RemoverRSupView.as_view(), name='RemoverRSup'),
    path('adicionar-lsup/<int:user_id>/', AdicionarLSupView.as_view(), name='AdicionarLSup'),
    path('remover-lsup/<int:user_id>/', RemoverLSupView.as_view(), name='RemoverLSup'),
    path('supervisores-guia/<int:pk>/editar/', GuiaSupervisoresEdit.as_view(), name='GuiaSupervisoresEditar'),
    path('supervisores-ações-todas/', SupervisoresOficial.as_view(), name='SupervisoresOficial'),
    path('supervisores-destaque/', CriarDestaque.as_view(), name='SupervisorDestaque'),
    path('palestra/<int:pk>/editar/', PalestraSupervisoresUpdateView.as_view(), name='PalestraEditar'),
    path('supervisores-ações/registrar/', RegistrarRelatorioSupervisor.as_view(), name='RegistrarRelatorioSupervisor'),
    path('supervisores-site/', SupSite.as_view(), name='SupSite')
]