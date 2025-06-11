import json
from django.http import HttpResponse
from productos.models import Producto

def agregar(request, *args, **kwargs):
    print("En la vista agregar")
    if request.method == "GET":
        idproducto = request.GET.get("cada_producto_id")
        valor = request.GET.get("valor")
        valor_local_storage = request.GET.get("cantidadGuardada")
        carro = request.session.get("carro")
        idproducto_rec = idproducto[5:]
        idproducto_rec = int(idproducto_rec)
        el_prod = Producto.objects.get(id=idproducto_rec)
        stock_disponible = int(el_prod.stock)-int(valor_local_storage)

        if stock_disponible >= int(valor):
            cantida = int(valor_local_storage)+int(valor)
        else:
            cantida = int(el_prod.stock)

    # ######################################################
    # ACTUALIZO VARIABLE DE SESSION
    # ######################################################

    carro[idproducto] = cantida
    request.session["carro"] = carro
    
    # ######################################################
    # # FIN
    # ######################################################

    print("Imprimo sesión carro: ")
    print(request.session["carro"])
    
    results = []
    data = {}
    data["idproducto"] = str(idproducto)
    data["cantida"] = str(cantida)
    results.append(data)
    data_json = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)