from django.urls import path
from .views import RePraça, AbrirRE, AbrirRM, RMOficial

urlpatterns = [
    path('recrutamentos/', RePraça.as_view(), name='RePraça'),
    path('recrutamento-abrir/', AbrirRE.as_view(), name='ReAbrir'),
    path('oficial/relatorio-de-movimento/abrir/', AbrirRM.as_view(), name='RMAbrir'),
    path('oficial/relatorio-de-movimento/', RMOficial.as_view(), name='RMOficial')
]