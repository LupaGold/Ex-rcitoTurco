from django.urls import path
from .views import Postagens, JornalPrincipal

urlpatterns = [
    path('principal/', JornalPrincipal.as_view(), name='JornalAlemao'),
    path('postagem/<slug:slug>/', Postagens.as_view(), name='PostagensJornal'),
]