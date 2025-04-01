# Dejamos la ruta del path
from django.urls import path
# Importamos la función creada
from bienvenida import views

urlpatterns = [
    path('',views.index, name='index'),
]
