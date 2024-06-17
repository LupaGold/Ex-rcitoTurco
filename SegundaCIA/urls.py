from django.urls import path
from .views import AvaliaçãoTPView, RegistrarTP, Relatório2CIAView, RegistrarRelatório2CIA, CriarDestaque2CIA

urlpatterns = [
    path('segunda-companhia/avaliação-tp/', AvaliaçãoTPView.as_view(), name='AvaliaçãoTP'),
    path('segunda-companhia/criar-destaque/', CriarDestaque2CIA.as_view(), name='CriarDestaque'),
    path('segunda-companhia/relatório-2cia/', Relatório2CIAView.as_view(), name='Relatório2CIA'),
    path('segunda-companhia/avaliação-tp/registrar/', RegistrarTP.as_view(), name='RegistrarTP'),
    path('segunda-companhia/relatório-2cia/registrar/', RegistrarRelatório2CIA.as_view(), name='RegistrarRelatório2CIA'),

]