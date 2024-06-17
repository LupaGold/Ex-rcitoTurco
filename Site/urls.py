from django.urls import path
from .views import SegundaCIA, SitePrincipal, DemitidosSite, PraçasEOficiais, AposentadosSite, PaginasLoad,PerfilMilitar

urlpatterns = [
    path('segunda-cia-treinamentos/', SegundaCIA.as_view(), name='SegundaCIA'),
    path('principal/', SitePrincipal.as_view(), name='PáginaPrincipal'),
    path('demitidos/', DemitidosSite.as_view(), name='Demitidos'),
    path('praças-e-oficiais/', PraçasEOficiais.as_view(), name='PraçasEOficiais'),
    path('aposentados/', AposentadosSite.as_view(), name='Aposentados'),
    path('<slug:slug>/', PaginasLoad.as_view(), name='PaginaUrl'),
    path('perfil/<slug:slug>/', PerfilMilitar.as_view(), name='PerfilMilitar'),
]