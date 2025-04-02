# Dejamos la ruta del path
from django.urls import path
# Importamos la función creada
from usuarios import views

urlpatterns = [
    path('',views.usuarios, name='usuarios'),
]
