from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .orcamentos.views import ItemViewSet, ClienteViewSet, OrcamentoViewSet
from django.contrib import admin

admin.autodiscover()

router = DefaultRouter()
router.register(r'itens', ItemViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'orcamentos', OrcamentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
