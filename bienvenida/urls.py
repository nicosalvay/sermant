# Dejamos la ruta del path
from django.urls import path
# Importamos la función creada
from bienvenida import views
from bienvenida.views import Index
from bienvenida.views import MensajeEnviado

urlpatterns = [
    #path('',views.index, name='index'),
    path('', Index.as_view(), name="index"),
    path('mensaje_enviado', MensajeEnviado.as_view(), name="mensaje_enviado"),
    #path('venta',views.venta, name='venta'),
]
