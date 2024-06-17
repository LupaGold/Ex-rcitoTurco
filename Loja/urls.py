from django.urls import path
from .views import (LojaEmblemasView, ComprarEmblemaView, MoedasMilitaresView, AddMoedasView, 
                    RemoveMoedasView, RegistrarEmblema, EditarEmblemas, EditarEmblemaView,
                    MoedasLoja, SaqueMoedas)

urlpatterns = [
    path('loja-emblemas/', LojaEmblemasView.as_view(), name='LojaEmblemas'),
    path('loja-moedas/', MoedasLoja.as_view(), name='MoedasLoja'),
    path('loja-moedas/sacar/<int:moeda_id>/', SaqueMoedas.as_view(), name='SaqueMoedas'),
    path('editar-emblema/', EditarEmblemas.as_view(), name='EditarEmblemas'),
    path('editar-emblema/<int:pk>/', EditarEmblemaView.as_view(), name='EditarEmblema'),
    path('registrar-emblema/', RegistrarEmblema.as_view(), name='RegistrarEmblema'),
    path('loja-emblemas/comprar/<int:emblema_id>/', ComprarEmblemaView.as_view(), name='ComprarEmblema'),
    path('militares/', MoedasMilitaresView.as_view(), name='MoedasMilitares'),
    path('adicionar-moedas/', AddMoedasView.as_view(), name='AdicionarMoedas'),
    path('remover-moedas/', RemoveMoedasView.as_view(), name='RemoverMoedas'),
]