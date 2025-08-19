from django.contrib.sitemaps import Sitemap
from productos.models import Producto

class ProductoSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Producto.objects.filter(estado='Activo')