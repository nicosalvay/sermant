import json
from django.http import HttpResponse

def quitar(request, *args, **kwargs):
    if request.method == "GET":
        idproducto = request.GET.get("cada_producto_id")
        valor = request.GET.get("valor")
        carro = request.session.get("carro")

        cantidad = int(valor) - 1
        # ###########################################
        # ACTUALIZO VARIABLE DE SESSION
        # ###########################################
        carro[idproducto] = cantidad
        request.session["carro"] = carro
        # ###########################################
        # FIN
        # ###########################################
        results = []
        data = {}
        data["idproducto"] = str(idproducto)
        data["cantidad"] = str(cantidad)
        results.append(data)
        data_json = json.dumps(results)
        mimetype = "application/json"
        return HttpResponse(data_json, mimetype)