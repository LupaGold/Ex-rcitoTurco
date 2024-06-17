from django.urls import path
from .views import (AjudanteOficial, AjudantePraça, RegistrarRelatorioAjudante, GuiaAjudantesView, GuiaAjudantesEdit,
                    PermissoesAjdView, AdicionarAjdView, AdicionarLAjdView, AdicionarRAjdView, RemoverAjdView, 
                    RemoverLAjdView, RemoverRAjdView, CriarDestaqueAjd)

urlpatterns = [
    path('ajudantes-ações/', AjudantePraça.as_view(), name='AjudantesPraça'),
    path('ajudantes-guia/', GuiaAjudantesView.as_view(), name='GuiaAjudantes'),
    path('ajudantes-permissões/', PermissoesAjdView.as_view(), name='PermissoesAjd'),
    path('adicionar-sup/<int:user_id>/', AdicionarAjdView.as_view(), name='AdicionarAjd'),
    path('remover-sup/<int:user_id>/', RemoverAjdView.as_view(), name='RemoverAjd'),
    path('adicionar-rsup/<int:user_id>/', AdicionarRAjdView.as_view(), name='AdicionarRAjd'),
    path('remover-rsup/<int:user_id>/', RemoverRAjdView.as_view(), name='RemoverRAjd'),
    path('adicionar-lsup/<int:user_id>/', AdicionarLAjdView.as_view(), name='AdicionarLAjd'),
    path('remover-lsup/<int:user_id>/', RemoverLAjdView.as_view(), name='RemoverLAjd'),
    path('ajudantes-guia/<int:pk>/editar/', GuiaAjudantesEdit.as_view(), name='GuiaAjudantesEditar'),
    path('ajudantes-ações-todas/', AjudanteOficial.as_view(), name='AjudantesOficial'),
    path('ajudantes-destaque/', CriarDestaqueAjd.as_view(), name='AjudantesDestaque'),
    path('ajudantes-ações/registrar/', RegistrarRelatorioAjudante.as_view(), name='RegistrarRelatorioAjd'),
]