from django.urls import path
from carro.views_carrito import Carrito
from carro import views_agregar
from carro import views_quitar

urlpatterns = [
    path("", Carrito.as_view(), name="carrito"),
    path("agregar/", views_agregar.agregar, name="agregar"),
    path("quitar/", views_quitar.quitar, name="quitar"),
]