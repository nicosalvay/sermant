from django.shortcuts import render
from productos.models import Producto
from productos.models import Categoria
from contacto.forms import ConsultaForm
from django.views.generic import View
from django.views.generic import FormView
# Create your views here.

class Index (FormView):
    #Creamos un diccionario
    template_name = 'bienvenida/index.html'
    form_class = ConsultaForm
    #success_url contiene la URL a la que se redirigirá al usuario después de que el formulario se haya enviado correctamente.
    success_url = 'mensaje_enviado'

    def get_context_data(self, **kwargs):
        params = super().get_context_data(**kwargs)
        params['palabras_claves'] = 'ascensores, mantenimiento, Córdoba, Ser-Mant'
        params['descripcion'] = 'Empresa líder en instalación y mantenimiento de ascensores en Córdoba.'
        return params

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    #form_valid es un método que se llama cuando el formulario es válido. Es un método de la clase FormView.
    def form_valid(self, form):
        form.save()
        form.send_email()
        return super().form_valid(form)

class MensajeEnviado(View):
    template_name = 'bienvenida/mensaje_enviado.html'

    def get(self, request):
        params = {
            'mensaje': 'Su mensaje ha sido enviado correctamente.',
            'palabras_claves': 'contacto, mensaje, Ser-Mant',
            'descripcion': 'Mensaje de contacto enviado correctamente en Ser-Mant.'
        }
        return render(request, self.template_name, params)

def venta (request):
    # Obtener todos los productos y categorías
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    # Crear un diccionario para pasar los datos a la plantilla
    params = {
        'nombre_sitio': 'Venta de Productos',
        'productos': productos,
        'categorias': categorias,
        'palabras_claves': 'productos, venta, ascensores, Ser-Mant',
        'descripcion': 'Catálogo de productos disponibles para la venta en Ser-Mant.'
    }

    return render (request, 'bienvenida/venta_productos.html',params)
