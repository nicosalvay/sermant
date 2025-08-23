"""
URL configuration for ascensores project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from tienda.sitemap import TiendaViewSitemap
from productos.sitemap import ProductoSitemap
from bienvenida.views import robots_view
from bienvenida.sitemap import BienvenidaViewSitemap
sitemaps = {
    'bienvenida': BienvenidaViewSitemap,
    'tienda': TiendaViewSitemap,
    'productos': ProductoSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    # Redirige la URL raíz al módulo bienvenida.urls
    path("", include('bienvenida.urls')),
    path('accounts/', include('registration.backends.default.urls')),
    path("usuarios/", include('usuarios.urls')),
    path("captcha/", include('captcha.urls')),
    path("tienda/", include ('tienda.urls')),
    path("api/v1.0/", include ('restapi.urls')),
    path("carrito/", include ('carro.urls')),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('robots.txt', robots_view, name='robots')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
