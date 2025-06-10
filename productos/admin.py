from django.contrib import admin
from productos.models import Producto
from productos.models import Categoria
from productos.models import ImgProducto
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render

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
    actions = ["activar_producto","exportar_a_json","ver_productos"]

    #queryset es el conjunto de datos que se selecciona desde el panel de administración
    def activar_producto(self, request, queryset):
        registro = queryset.update(estado="Activo")
        if registro == 1:
            mensaje = "1 registro actualizado"
        else:
            mensaje = "%s registros actualizados" % registro
        self.message_user(request, "%s exitosamente" % mensaje)


    #Esta función se ejecuta cuando se selecciona la acción desde el panel de administración
    activar_producto.short_description = "Pasar a activo"
    
    def exportar_a_json(self, request, queryset):
        # queryset es el conjunto de datos que se selecciona desde el panel de administración
        response = HttpResponse(content_type="application/json")
        #serializers es un módulo de Django que permite convertir objetos de Python a otros formatos como JSON, XML, etc.
        serializers.serialize("json", queryset, stream=response)
        return response
    
    def ver_productos(self, request, queryset):
        params={}
        productos = queryset
        params["productos"]=productos
        return render(request, "admin/productos/productos_seleccionados.html", params)

    ver_productos.short_description = "Ver productos"


    
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

