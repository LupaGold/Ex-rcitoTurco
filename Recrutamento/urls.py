from django.urls import path
from .views import RePraça, AbrirRE

urlpatterns = [
    path('recrutamentos/', RePraça.as_view(), name='RePraça'),
    path('recrutamento-abrir/', AbrirRE.as_view(), name='ReAbrir'),
]