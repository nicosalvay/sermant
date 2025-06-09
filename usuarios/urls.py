# Dejamos la ruta del path
from django.urls import path
# Importamos la función creada
from usuarios import views
from usuarios.views import ModUsuarios

urlpatterns = [
    path('usuarios',ModUsuarios.as_view(), name='usuarios'),
]
