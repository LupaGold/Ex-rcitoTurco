from django.contrib import admin
from .models import SupervisorRelatorio, GuiaSupervisores, DestaqueSupervisor, PalestraSupervisores
# Register your models here.
admin.site.register(SupervisorRelatorio)
admin.site.register(GuiaSupervisores)
admin.site.register(DestaqueSupervisor)
admin.site.register(PalestraSupervisores)