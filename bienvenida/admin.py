from django.contrib import admin
from .models import Producto
from .models import Categoria

# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    "Mostrar el campo categoría primero en el panel admin de productos y dividir los campos en secciones"
    fieldsets = [
    ("Relación", {"fields":["categoria"]}),
    (
        "Datos generales",
        {
            "fields":[
                "producto",
                "descripcion","stock",
                "fecha_publicacion","precio",
                "estado","imagen"
            ]
        },
    ),
    ]
    list_display = ("producto", "categoria", "fecha_publicacion", "estado_de_producto","stock","precio")
    ordering = ("producto",)
    list_filter = ("estado", "categoria")
    search_fields = ("producto", )
    list_display_links = ("producto", "fecha_publicacion", "categoria")

# Permite incluir modelos relacionados de forma tabular (en filas)
class ProductoInline (admin.TabularInline):
    model = Producto
    extra = 0

class CategoriaAdmin (admin.ModelAdmin):
    inlines = [ProductoInline]


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria,CategoriaAdmin)
