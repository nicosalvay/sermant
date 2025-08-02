from productos.models import Producto
from rest_framework import serializers

class ProductosRestApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
