from django.urls import path
from .views import PrincipalView


urlpatterns = [
    path('principal/', PrincipalView.as_view(), name='PrincipalPainel'),
]