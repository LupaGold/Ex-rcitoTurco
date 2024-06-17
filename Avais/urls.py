from django.urls import path
from .views import AvalPraça, RegistrarAval, AvalAC, AprovarJAView, RejeitarJAView

urlpatterns = [
    path('avais/', AvalPraça.as_view(), name='AvalPraça'),
    path('registrar-aval/', RegistrarAval.as_view(), name='RegistrarAval'),
    path('avais-todos/', AvalAC.as_view(), name='AvalAC'),
    path('avais-todos/aprovar/<int:ja_id>/', AprovarJAView.as_view(), name='AprovarAval'),
    path('avais-todos/rejeitar/<int:ja_id>/', RejeitarJAView.as_view(), name='RejeitarAval'),
]