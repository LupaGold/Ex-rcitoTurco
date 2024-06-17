from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from Site.models import PaginaSite
from Supervisores.models import GuiaSupervisores
from Ajudantes.models import GuiaAjudantes
from Painel.models import DestaqueOficial, DestaquePraça

class UpdateLastAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            request.user.last_accessed = timezone.now()
            request.user.save()
        return response
    
class GroupContextMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        
        patentes_ac = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
        ]

        patentes_ofc = [
            'Marechal ★★★★★',
            'General-de-Exército ★★★★',
            'General-de-Divisão ★★★',
            'General-de-Brigada ★★',
            'Coronel ★',
            'Tenente-Coronel',
            'Major',
            'Capitão',
            'Segundo Tenente',
            'Primeiro Tenente',
        ]
        user = request.user.patente if request.user.is_authenticated else None
        response.context_data['OFC'] = user in patentes_ofc if patentes_ofc else False
        response.context_data['AC'] = user in patentes_ac if patentes_ac else False
        response.context_data['JORNALISTA'] = request.user.groups.filter(name='JORNALISTA').exists()
        response.context_data['LJORNALISTA'] = request.user.groups.filter(name='LJORNALISTA').exists()
        response.context_data['LSUP'] = request.user.groups.filter(name='LSUP').exists()
        response.context_data['RSUP'] = request.user.groups.filter(name='RSUP').exists()
        response.context_data['SUP'] = request.user.groups.filter(name='SUP').exists()
        response.context_data['LAJD'] = request.user.groups.filter(name='LAJD').exists()
        response.context_data['RAJD'] = request.user.groups.filter(name='RAJD').exists()
        response.context_data['AJD'] = request.user.groups.filter(name='AJD').exists()
        response.context_data['ei'] = PaginaSite.objects.all().filter(categoria='Escolas e Institutos').order_by('ordenador')
        response.context_data['apostilas'] = PaginaSite.objects.all().filter(categoria='Apostilas').order_by('ordenador')
        response.context_data['grupos'] = PaginaSite.objects.all().filter(categoria='Grupos').order_by('ordenador')
        response.context_data['hierarquia'] = PaginaSite.objects.all().filter(categoria='Hierarquia')
        response.context_data['TeamSpeak'] = PaginaSite.objects.all().filter(categoria='Team Speak')
        response.context_data['guiasup'] = GuiaSupervisores.objects.last()
        response.context_data['guiaajd'] = GuiaAjudantes.objects.last()
        response.context_data['destpraca'] = DestaquePraça.objects.last()
        response.context_data['destofc'] = DestaqueOficial.objects.last()
        return response