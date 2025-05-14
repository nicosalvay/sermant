from django.contrib import admin
from contacto.models import Consulta
from contacto.models import Respuesta

class RespuestaInline(admin.TabularInline):
    model=Respuesta
    extra=0

class ConsultaAdmin(admin.ModelAdmin):
    inlines=[RespuestaInline]
    list_display=['estado_de_respuesta', 'nombre', 'apellido', 'cod_area','email', 'telefono', 'fecha_contacto']
    list_filter=['estado_respuesta', 'fecha_contacto']

admin.site.register(Consulta, ConsultaAdmin)
