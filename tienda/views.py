from django.shortcuts import render
from django.template.loader import render_to_string
from tienda.forms import CargaProducto, ImagenesProductoFormSet
from productos.models import Producto, Categoria, ImgProducto
from django.shortcuts import redirect
from django.http import Http404, JsonResponse, HttpResponse
from django.views.generic import View
from productos.forms import SearchProductoForm

def cargar_producto(request):
    params={}
    # Metadatos para SEO
    params['palabras_claves'] = 'cargar producto, tienda, Ser-Mant'
    params['descripcion'] = 'Formulario para cargar nuevos productos en la tienda Ser-Mant.'

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

    # Define tu propio método para verificar AJAX
    def is_ajax(self, request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    
    def get(self, request):
        params={}
        search_form = SearchProductoForm(request.GET) #
        productos = Producto.objects.all() #
        categorias_seleccionadas_ids_str = request.GET.getlist('categorias') #

        query = request.GET.get('querycom', '').strip() #
        if query: #
            from django.db.models import Q # Importa Q aquí si no lo hiciste arriba
            productos = productos.filter(
                Q(producto__icontains=query) | Q(descripcion__icontains=query) # Asumo que también filtras por descripción
            ).distinct()

        if categorias_seleccionadas_ids_str: #
            try: #
                categorias_seleccionadas_ids_int = [int(cat_id) for cat_id in categorias_seleccionadas_ids_str] #
                productos = productos.filter(categoria__id__in=categorias_seleccionadas_ids_int).distinct() #
            except ValueError: #
                print("Advertencia: Se recibió un ID de categoría no válido.") #
                pass #

        precio_desde = request.GET.get('precioDesde') #
        precio_hasta = request.GET.get('precioHasta') #
        if precio_desde: #
            try: #
                productos = productos.filter(precio__gte=float(precio_desde)) #
            except ValueError: #
                pass #
        if precio_hasta: #
            try: #
                productos = productos.filter(precio__lte=float(precio_hasta)) #
            except ValueError: #
                pass #

        # Re-obtener categorías para el sidebar, etc.
        try: #
            categorias = Categoria.objects.all() #
            # imagenes = ImgProducto.objects.all() # No necesitas todas las imágenes aquí si las obtienes por producto
        except Exception as e: #
            print(f"Error al obtener categorías: {e}") #
            raise Http404("No se pudieron cargar recursos esenciales.") #

        # --- Determinar si la petición es AJAX o una carga de página completa ---
        if self.is_ajax(request):
            # Es una petición AJAX, devuelve el HTML renderizado de los productos
            contexto_parcial = {
                'productos': productos,
            }

            html_productos = render_to_string(
                'tienda/_product_cards.html', # <--- Ruta a tu nuevo archivo parcial
                contexto_parcial,
                request=request # Importante para que {% csrf_token %} y {% url %} funcionen en el parcial
            )

            if not productos.exists(): # Si no hay productos, mostrar un mensaje
                 html_productos = '<div class="col-12"><p class="text-white text-center">No se encontraron productos que coincidan con tu búsqueda.</p></div>'

            return JsonResponse({'html': html_productos}) # Envía el HTML como parte de una respuesta JSON
        else:
            # Es una carga de página normal, renderiza la plantilla HTML completa
            params = {
                'nombre_sitio': 'Venta de Productos',
                'productos': productos, # 'productos' ya viene filtrado aquí
                'categorias': categorias, # Pasa todas las categorías para los checkboxes
                # 'imagenes': imagenes, # Ya no necesitas pasar todas las imágenes aquí si se cargan por producto
                'search': search_form, # Pasa el formulario para que el input mantenga el valor
                'selected_category_ids': categorias_seleccionadas_ids_str, # Para mantener los checkboxes marcados
                # Metadatos para SEO
                'palabras_claves': 'venta, productos, tienda, Ser-Mant',
                'descripcion': 'Catálogo de productos disponibles para la venta en Ser-Mant.'
            }

        # ###############################################################
        # INICIALIZAR LA VARIABLE DE SESSION CARRO (Mantenemos esta lógica)
        # ###############################################################
        try:
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
    # Metadatos para SEO
    params['palabras_claves'] = 'ver imagen, producto, tienda, Ser-Mant'
    params['descripcion'] = 'Visualiza las imágenes asociadas a un producto en la tienda Ser-Mant.'
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

