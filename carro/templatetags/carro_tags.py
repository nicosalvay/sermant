from django import template

# Esta línea es para registrar los filtros y etiquetas
register = template.Library()

@register.filter(name="carro_cantida")
def carro_cantida(producto, carro):
    """
    Filtro de plantilla que devuelve la cantidad de un producto
    específico en el carrito de la sesión.
    """
    # Asegúrate de que 'carro' es un diccionario antes de intentar usar .get()
    if not isinstance(carro, dict):
        return 0

    # La clave en el diccionario del carrito es "prod_ID"
    key = f"prod_{producto.pk}"
    
    # Usa .get() para buscar la clave; si no existe, devuelve el valor por defecto (0)
    cantidad = carro.get(key, 0)
    
    # El valor puede venir como una cadena (por el localStorage), así que lo
    # convertimos a un entero.
    try:
        return int(cantidad)
    except (ValueError, TypeError):
        # Si la conversión falla (por una cadena vacía o no numérica),
        # devolvemos 0 para evitar errores.
        return 0
    
@register.filter(name="precio_total_producto")
def precio_total_producto(producto, carro):
    """
    Calcula el precio total de un solo producto, multiplicando su precio
    por la cantidad que tiene en el carrito.
    """
    # Asegúrate de que 'carro' es un diccionario antes de intentar usarlo
    if not isinstance(carro, dict):
        return "{0:.2f}".format(0) # Devuelve 0 formateado si el carro no es válido

    # Usamos el filtro 'carro_cantida' para obtener la cantidad
    cantidad = carro_cantida(producto, carro)
    
    # Si la cantidad es 0, el total es 0
    if cantidad == 0:
        return "{0:.2f}".format(0)
    
    # Si no tienes descuentos, simplemente haz la multiplicación
    total = producto.precio * cantidad
    
    # Formateamos el resultado a dos decimales para que se vea como dinero
    return "{0:.2f}".format(total)

@register.simple_tag(name="carro_total_cantidad")
def carro_total_cantidad(carro):
    """
    Devuelve la cantidad total de productos seleccionados en el carrito.
    """
    total = 0
    # Asegúrate de que 'carro' es un diccionario antes de intentar iterar
    if isinstance(carro, dict):
        for key, value in carro.items():
            if key.startswith("prod_"):
                try:
                    total += int(value)
                except (ValueError, TypeError):
                    # Ignorar valores no numéricos o si hay un error de tipo
                    continue
    return total


# TOTAL GLOBAL
# *** Modificado para ser un FILTRO ***
@register.filter(name="carro_total_global")
def carro_total_global(productos_list, carro_session):
    """
    Calcula el precio total de todos los productos en el carrito,
    sumando el total de cada producto.
    """
    total_global = 0
    # Asegúrate de que 'carro_session' es un diccionario antes de intentar usarlo
    if isinstance(carro_session, dict):
        for producto in productos_list:
            product_id_in_cart_key = f"prod_{producto.id}"
            
            cantidad_en_carro = 0
            try:
                # Usa .get() para evitar errores si el producto no está en el carrito
                cantidad_en_carro = int(carro_session.get(product_id_in_cart_key, 0))
            except (ValueError, TypeError):
                cantidad_en_carro = 0 
            
            # Calcula el total para este producto específico y lo suma al total global
            # Asume que 'producto.precio' está disponible en el objeto producto
            total_por_este_producto = float(producto.precio) * cantidad_en_carro # Convertir a float por seguridad
            total_global += total_por_este_producto
    
    # Formatear el resultado final a dos decimales
    return "{0:.2f}".format(total_global)