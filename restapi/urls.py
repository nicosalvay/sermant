from rest_framework import routers
from .viewsets import ProductosRestApiViewSet
router = routers.SimpleRouter()
router.register('productosrestapi', ProductosRestApiViewSet)
urlpatterns = router.urls
