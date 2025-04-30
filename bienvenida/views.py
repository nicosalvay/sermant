from django.shortcuts import render
from productos.models import Producto
from productos.models import Categoria

# Create your views here.

def index (request):
    #Creamos un diccionario
    params = {}
    params ['nombre_sitio'] = 'Pagina Bienvenida'
    return render (request, 'bienvenida/index.html',params)

def venta (request):
    # Obtener todos los productos y categorías
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    # Crear un diccionario para pasar los datos a la plantilla
    params = {
        'nombre_sitio': 'Venta de Productos',
        'productos': productos,
        'categorias': categorias,
    }

    return render (request, 'bienvenida/venta_productos.html',params)
