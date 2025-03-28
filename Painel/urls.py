from django.urls import path
from .views import PrincipalView, RegimentoView, FAQView, InfoView, Ranking


urlpatterns = [
    path('principal/', PrincipalView.as_view(), name='PrincipalPainel'),
    path('oficiais/regimento/', RegimentoView.as_view(), name='Regimento'),
    path('oficiais/informações/', InfoView.as_view(), name='Informações'),
    path('oficiais/FAQ/', FAQView.as_view(), name='FAQ'),
    path('oficiais/Ranking/', Ranking.as_view(), name='Ranking')
]