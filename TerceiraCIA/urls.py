from django.urls import path
from .views import Relatório3CIAView, CriarDestaque3CIA, RegistrarRelatório3CIA, Doação3CIAView, RegistrarDoação3CIA

urlpatterns = [
    path('terceira-companhia/relatório/', Relatório3CIAView.as_view(), name='Relatório3CIA'),
    path('terceira-companhia/criar-destaque/', CriarDestaque3CIA.as_view(), name='CriarDestaque3CIA'),
    path('terceira-companhia/relatório-3cia/', RegistrarRelatório3CIA.as_view(), name='RegistrarRelatório3CIA'),
    path('terceira-companhia/doação/registrar/', Doação3CIAView.as_view(), name='Doação3CIA'),
    path('terceira-companhia/doação/', RegistrarDoação3CIA.as_view(), name='RegistrarDoação3CIA'),

]