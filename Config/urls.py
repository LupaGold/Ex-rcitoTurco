from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url=reverse_lazy('PáginaPrincipal'))),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('', include('ConAcs.urls')),
    path('painel/', include('Painel.urls')),
    path('painel/', include('Avais.urls')),
    path('painel/', include('Treinamentos.urls')),
    path('', include('Site.urls')),
    path('painel/', include('TerceiraCIA.urls')),
    path('painel/', include('SegundaCIA.urls')),
    path('painel/', include('Supervisores.urls')),
    path('painel/', include('Ajudantes.urls')),
    path('painel/', include('Loja.urls')),
    path('jornal/', include('Jornal.urls')),
    path('painel/', include('Recrutamento.urls')),
    path('painel/', include('Monitores.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
