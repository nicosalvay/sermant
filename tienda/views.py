from django.shortcuts import render
from tienda.forms import CargaProducto, ImagenesProductoFormSet
from productos.models import Producto, Categoria, ImgProducto
from django.shortcuts import redirect
from django.http import Http404
from django.views.generic import View
 
def cargar_producto(request):
    params={}

    if request.method == 'POST':
        # Si el método es POST, se procesa el formulario
        # Se crea una instancia del formulario con los datos POST y los archivos
        form = CargaProducto(request.POST, request.FILES)
        imagenes_formset = ImagenesProductoFormSet(request.POST, request.FILES)
        #imagenes_formset = ImagenesProductoFormSet(request.POST, request.FILES)
        params['form'] = form
        # Se verifica si el formulario es válido
        # Si el formulario es válido, se guarda el nuevo producto
        print("Formulario recibido")
        # <--- ¡Aquí debes colocar los prints! --->
        print("Errores del formulario:", form.errors)
        print("Errores del formset:", imagenes_formset.errors)
        #if form.is_valid():
        if form.is_valid() and imagenes_formset.is_valid():
            print("Formulario y formset válidos")
            producto = form.cleaned_data['producto']
            descripcion = form.cleaned_data['descripcion']
            stock = form.cleaned_data['stock'] 
            fecha_publicacion = form.cleaned_data['fecha_publicacion']
            precio = form.cleaned_data['precio']
            estado = form.cleaned_data['estado']
            imagen = form.cleaned_data['imagen']
            categoria = form.cleaned_data['categoria']
            #producto_estado = form.cleaned_data['producto__estado']
            #producto_imagen = form.cleaned_data['producto__imagen']

            nuevo_producto = Producto(producto=producto, descripcion=descripcion, stock=stock,
                                      fecha_publicacion=fecha_publicacion, precio=precio, estado=estado, imagen=imagen, categoria=categoria)
            nuevo_producto.save()
            # Guardar las imágenes asociadas al producto
            # Guarda las imágenes relacionadas a través del formset
            imagenes = imagenes_formset.save(commit=False)
            for imagen in imagenes:
                imagen.producto = nuevo_producto
                imagen.estado = form.cleaned_data['estado']  # Guarda el estado de la imagen
                imagen.save()

            # Se redirige a la vista de índice después de guardar el producto
            print("Producto e imágenes guardados")
            return redirect('index')

    else:
        print("Método GET")
        # Si el método no es POST (es un GET), se crea un formulario vacío
        form = CargaProducto()
        imagenes_formset = ImagenesProductoFormSet()  # Crea una instancia del formset en el GET
        params['form'] = form
        params['imagenes_formset'] = imagenes_formset  # Pasa el formset al template en el GET
        return render(request, 'tienda/formulario.html', params)

class VentaProductos(View):
    template = 'tienda/venta_productos.html'
    
    def get(self, request):
        params={}
        try:
            # Se obtienen todos los productos de la base de datos
            # Se utiliza el método all() para obtener todos los objetos de la clase Producto
            productos = Producto.objects.all()
            categorias = Categoria.objects.all()
            imagenes = ImgProducto.objects.all()
        except Producto.DoesNotExist:
            raise Http404
        params = {
        'nombre_sitio': 'Venta de Productos',
        'productos': productos,
        'categorias': categorias,
        'imagenes': imagenes,
        }
        # ###############################################################
        # INICIALIZAR LA VARIABLE DE SESSION CARRO
        # ###############################################################
        try:
            #request.session es un diccionario que almacena datos de sesión
            # y se utiliza para almacenar información específica del usuario
            request.session["carro"]
        except:
            request.session["carro"] = {}

        return render(request, self.template, params)

    def post(self, request):
        params = {}
        producto=request.POST.get("producto")

        #request.session.get("el_pedido") obtiene el valor de la sesión "el_pedido" que se creó en el método GET.
        # Si la sesión "el_pedido" existe, se obtiene su valor. Si no existe, se crea un nuevo diccionario vacío.
        el_pedido = request.session.get("el_pedido")
        if el_pedido:
            
            cantidad = el_pedido.get(producto)
            if cantidad:
                el_pedido[producto]=cantidad+1
            else:
                el_pedido[producto]=1
        else:
            el_pedido={}
            el_pedido[producto]=1

        request.session["el_pedido"]=el_pedido
        print(request.session["el_pedido"])

        return redirect("venta_productos")

def ver_imagen(request, producto_id):
    # Se obtiene el producto por su ID 
    params={}
    try:
        # Se busca el producto en la base de datos por su ID
        # Se utiliza el método get() para obtener un objeto específico de la clase Producto
        producto = Producto.objects.get(pk=producto_id)
        imagenes = ImgProducto.objects.all()
    except Producto.DoesNotExist:
        # Si no se encuentra el producto, se lanza una excepción Http404
        raise Http404
    params["producto"] = producto
    params["imagenes"] = imagenes
    return render(request, "tienda/verimagen.html", params)

