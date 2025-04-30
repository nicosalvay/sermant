from django.contrib import admin
from productos.models import Producto
from productos.models import Categoria
from productos.models import ImgProducto

# Register your models here.

class ImgProductoInline (admin.TabularInline):
    model = ImgProducto
    extra = 0

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
    inlines = [ImgProductoInline]    
    
class ImgProductoAdmin (admin.ModelAdmin):
    "Mostrar el campo categoría primero en el panel admin de productos y dividir los campos en secciones"
    fieldsets = [
    ("Relación", {"fields":["producto"]}),
    (
        "Datos generales",
        {
            "fields":[
                "estado",
                "imagen"
            ]
        },
    ),
    ]
    list_display = ("producto", "estado","imagen")
    ordering = ("producto",)
    list_filter = ("estado", "producto")
    search_fields = ("producto", )
    list_display_links = ("producto",)

# Permite incluir modelos relacionados de forma tabular (en filas)
class ProductoInline (admin.TabularInline):
    model = Producto
    extra = 0

class CategoriaAdmin (admin.ModelAdmin):
    inlines = [ProductoInline]


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria,CategoriaAdmin)
admin.site.register(ImgProducto, ImgProductoAdmin)

