import json
from django.http import HttpResponse
import ast


def crear_localstorage(request, *args, **kwargs):
    if request.method == "GET":
        person = request.GET
        """ ######################################
        # CONVERTIR FORMATO DE JSON A DICCIONARIO
        # Y GUARDAR EN VARIABLE DE SESSION
        ##########################################"""
        producto_formato_diccionario = person.dict()
        producto_dict = ast.literal_eval(producto_formato_diccionario["producto"])
        request.session["carro"] = producto_dict
        results = []
        data = {}
        data_json = json.dumps(results)
        mimetype = "application/json"
        # Retorna un json vacío
        return HttpResponse(data_json, mimetype)
