from django.contrib import admin
from usuarios.models import Datousuario

class DatoUsuarioAdmin(admin.ModelAdmin):
    "Mostrar el campo usuario primero en el panel admin de usuarios y dividir los campos en secciones"
    fieldsets = [
        (
            "Información adicional",
            {
                "fields": [
                    "imagen",
                    "fecha_nacimiento",
                    "pais",
                    "provincia",
                    "ciudad",
                    "domicilio",
                    "codigo_postal",
                    "telefono",
                    "celular",
                    "documento",
                    "cuit"
                ]
            },
        ),
    ]
    list_display = ("usuario", "fecha_nacimiento", "pais", "provincia", "ciudad")
    ordering = ("usuario",)
    
# Register your models here.
admin.site.register(Datousuario, DatoUsuarioAdmin)
