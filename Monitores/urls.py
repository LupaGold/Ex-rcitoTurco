from django.urls import path
from .views import (
    MonitorPraça, GuiaMonitoresView, GuiaMonitoresEdit, CriarDestaqueMonitores, RegistrarRelatorioMonitores,
    MonitorOficial, AdicionarLMNTView, AdicionarMNTView, AdicionarRMNTView, RemoverLMNTView, RemoverMNTView, RemoverRMNTView, PermissoesMNTView)

urlpatterns = [
    path('monitor-ações/', MonitorPraça.as_view(), name='MonitoresPraça'),
    path('monitor-ações/oficiais/', MonitorOficial.as_view(), name='MonitoresOficial'),
    path('monitor-guia/', GuiaMonitoresView.as_view(), name='GuiaMonitores'),
    path('monitor-guia/<int:pk>/editar/', GuiaMonitoresEdit.as_view(), name='EditarGuiaMonitores'),
    path('monitor-destaque/criar/', CriarDestaqueMonitores.as_view(), name='MonitorDestaqueCriar'),
    path('monitor-ações/registrar/', RegistrarRelatorioMonitores.as_view(), name='MonitoresRegistrarAção'),
    path('monitores-permissões/', PermissoesMNTView.as_view(), name='Permissoesmnt'),
    path('adicionar-mnt/<int:user_id>/', AdicionarMNTView.as_view(), name='Adicionarmnt'),
    path('remover-mnt/<int:user_id>/', RemoverMNTView.as_view(), name='Removermnt'),
    path('adicionar-rmnt/<int:user_id>/', AdicionarRMNTView.as_view(), name='AdicionarRmnt'),
    path('remover-rmnt/<int:user_id>/', RemoverRMNTView.as_view(), name='RemoverRmnt'),
    path('adicionar-lmnt/<int:user_id>/', AdicionarLMNTView.as_view(), name='AdicionarLmnt'),
    path('remover-lmnt/<int:user_id>/', RemoverLMNTView.as_view(), name='RemoverLmnt'),
]