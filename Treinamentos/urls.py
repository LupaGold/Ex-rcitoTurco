from django.urls import path
from .views import RelatorioPraça, RegistrarRelatorio, RelatorioOficial, AprovarRelatorio, ReprovarRelatorio

urlpatterns = [
    path('relatorios/', RelatorioPraça.as_view(), name='RelatoriosDeTreinamento'),
    path('registrar-relatorio/', RegistrarRelatorio.as_view(), name='RegistrarRelatorio'),
    path('relatorios-todos/', RelatorioOficial.as_view(), name='RelatoriosOficiais'),
    path('relatorios-todos/aprovar/<int:relatorio_id>/', AprovarRelatorio.as_view(), name='AprovarRelatorio'),
    path('relatorios-todos/reprovar/<int:relatorio_id>/', ReprovarRelatorio.as_view(), name='ReprovarRelatorio'),
]