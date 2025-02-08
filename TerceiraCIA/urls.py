from django.urls import path
from .views import Relatório3CIAView, Permissoes3ciaview,CriarDestaque3CIA, RegistrarRelatório3CIA, Doação3CIAView, RegistrarDoação3CIA, AdicionarL3CIA, AdicionarM3CIA, RemoverL3CIA, RemoverM3CIA

urlpatterns = [
    path('terceira-companhia/relatório/', Relatório3CIAView.as_view(), name='Relatório3CIA'),
    path('terceira-companhia/criar-destaque/', CriarDestaque3CIA.as_view(), name='CriarDestaque3CIA'),
    path('terceira-companhia/relatório-3cia/', RegistrarRelatório3CIA.as_view(), name='RegistrarRelatório3CIA'),
    path('terceira-companhia/doação/registrar/', Doação3CIAView.as_view(), name='Doação3CIA'),
    path('terceira-companhia/doação/', RegistrarDoação3CIA.as_view(), name='RegistrarDoação3CIA'),
    path('terceira-companhia/adicionar-m3cia/<int:user_id>/', AdicionarM3CIA.as_view(), name='Adicionarm3cia'),
    path('terceira-companhia/remover-m3cia/<int:user_id>/', RemoverM3CIA.as_view(), name='Removerm3cia'),
    path('terceira-companhia/adicionar-l3cia/<int:user_id>/', AdicionarL3CIA.as_view(), name='Adicionarl3cia'),
    path('terceira-companhia/remover-l3cia/<int:user_id>/', RemoverL3CIA.as_view(), name='Removerl3cia'),
    path('terceira-companhia/permissões/', Permissoes3ciaview.as_view(), name='Permi3CIA'),

]