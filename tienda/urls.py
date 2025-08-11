from django.urls import path
from tienda import views
from tienda.views import VentaProductos
from tienda import views_agregar
from tienda.views_busqueda import BuscarProducto
from tienda import crear_datos_localstorage

urlpatterns = [
    path('cargar/', views.cargar_producto, name="carga_producto"),
    #Declaramos el id del producto como parte de la url
    path('<int:producto_id>/ver/', views.ver_imagen, name="ver_producto"),
    path('venta_productos/', VentaProductos.as_view(), name="venta_productos"),
    path("agregar/", views_agregar.agregar, name="agregar"),
    path("buscar_producto", BuscarProducto.as_view(), name="buscar_producto"),
    path(
        "crear_localstorage/",
        crear_datos_localstorage.crear_localstorage,
        name="crear_localstorage",
    ),    
]
