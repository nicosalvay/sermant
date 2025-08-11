from django.contrib import sitemaps
from django.urls import reverse

class TiendaViewSitemap(sitemaps.Sitemap):
    priority = 0.9 # Prioridad de la página
    changefreq = 'daily' # Frecuencia de cambio de la página
    def items(self):
        return ['venta_productos',] # Lista de vistas que se incluirán en el sitemap
    def location(self, item):
        return reverse(item)