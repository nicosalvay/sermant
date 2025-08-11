from django import template

# Esta línea es para registrar los filtros y etiquetas
register = template.Library()

@register.filter(name="carro_cantida")
def carro_cantida(producto, carro):
    """
    Filtro de plantilla que devuelve la cantidad de un producto
    específico en el carrito de la sesión.
    """
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
    # Usamos el filtro 'carro_cantida' para obtener la cantidad
    cantidad = carro_cantida(producto, carro)
    
    # Si la cantidad es 0, el total es 0
    if cantidad == 0:
        return 0
    
    # Si no tienes descuentos, simplemente haz la multiplicación
    total = producto.precio * cantidad
    
    # Formateamos el resultado a dos decimales para que se vea como dinero
    return "{0:.2f}".format(total)
    