from django.urls import path
from .views import AvaliaçãoTPView, RegistrarTP, Relatório2CIAView, RegistrarRelatório2CIA, CriarDestaque2CIA, AdicionarM2CIA, AdicionarL2CIA, RemoverL2CIA, RemoverM2CIA, Permissoes2ciaview

urlpatterns = [
    path('segunda-companhia/avaliação-tp/', AvaliaçãoTPView.as_view(), name='AvaliaçãoTP'),
    path('segunda-companhia/criar-destaque/', CriarDestaque2CIA.as_view(), name='CriarDestaque'),
    path('segunda-companhia/relatório-2cia/', Relatório2CIAView.as_view(), name='Relatório2CIA'),
    path('segunda-companhia/avaliação-tp/registrar/', RegistrarTP.as_view(), name='RegistrarTP'),
    path('segunda-companhia/relatório-2cia/registrar/', RegistrarRelatório2CIA.as_view(), name='RegistrarRelatório2CIA'),
    path('segunda-companhia/adicionar-m2cia/<int:user_id>/', AdicionarM2CIA.as_view(), name='Adicionarm2cia'),
    path('segunda-companhia/remover-m2cia/<int:user_id>/', RemoverM2CIA.as_view(), name='Removerm2cia'),
    path('segunda-companhia/adicionar-l2cia/<int:user_id>/', AdicionarL2CIA.as_view(), name='Adicionarl2cia'),
    path('segunda-companhia/remover-l2cia/<int:user_id>/', RemoverL2CIA.as_view(), name='Removerl2cia'),
    path('segunda-companhia/permissões/', Permissoes2ciaview.as_view(), name='Permi2CIA'),

]