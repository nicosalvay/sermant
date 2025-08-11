from django.urls import path
from carro.views_carrito import Carrito

urlpatterns = [
    path("", Carrito.as_view(), name="carrito"),
]