from rest_framework import viewsets
from productos.models import Producto
from .serializer import ProductosRestApiSerializer

class ProductosRestApiViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductosRestApiSerializer
