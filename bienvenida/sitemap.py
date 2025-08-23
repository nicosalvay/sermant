from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class BienvenidaViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        # Nombres de las vistas que quieres incluir
        return ['index']

    def location(self, item):
        return reverse(item)