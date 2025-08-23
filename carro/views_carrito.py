from productos.models import Producto
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db.models import Q
from usuarios.models import Datousuario
from django.contrib.sites.models import Site

class Carrito(View):
    template = "carro/carrito.html"

    def get(self, request):
        params = {}   
        ids = list(request.session.get("carro").keys())
        ids2 = []

        # Limpio los ids de productos que vienen de la variable de sesión con prod_xxx. 
        for id in ids:
            print(id[:4])
            if id[:4] == "prod":
                val = id[5:]
                val = int(val)
                ids2.append(val)     
 
        # ##########################################################
        # PARA USUARIO
        # ###########################################################
        # user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        # ##########################################################
        # PARA USUARIO
        # ###########################################################
        art_venta = Producto.objects.filter(pk__in=ids2)
        print(art_venta)
        params["productos"] = art_venta
        # ##########################################################
        # PARA USUARIO
        # ###########################################################
        if request.user.is_authenticated:
            params["usuario"] = request.user
        """    
            try:
                datos_para_imagen = Perfil.objects.get(usuario=request.user.pk)
                params["datos_para_imagen"] = datos_para_imagen
            except ObjectDoesNotExist:
                pass
        """
        # ##########################################################
        # PARA RUTAS EN LINKS
        # ###########################################################
        current_site = Site.objects.get_current()
        params["dominio_actual"] = current_site.domain
        params["palabras_claves"] = "carrito, productos, compra, Ser-Mant"
        params["descripcion"] = "Visualiza y gestiona los productos en tu carrito de compras en Ser-Mant."
        return render(request, self.template, params)