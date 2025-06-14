import json
from django.http import HttpResponse
from django.views.generic import View
from productos.models import Producto

class BuscarProducto(View):
    template = "tienda/buscar_producto.html"

    # Define tu propio método para verificar AJAX
    def is_ajax(self, request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def get(self, request):
        if self.is_ajax(request=request):
            palabra=request.GET.get('term', '')
            print(palabra)
            producto=Producto.objects.filter(producto__icontains=palabra)
            result=[]
            for prod in producto:
                data={}
                data['label']=prod.producto
                result.append(data)
            data_json=json.dumps(result)
        else:
            data_json="fallo"
        mimetype="application/json"
        return HttpResponse(data_json, mimetype)
