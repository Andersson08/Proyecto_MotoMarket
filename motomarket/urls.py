from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

admin.site.site_header = "MotoMarket – Administración"
admin.site.site_title = "MotoMarket"
admin.site.index_title = "Panel del concesionario"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("cuenta/", include("usuarios.urls")),
    path("motos/", include("catalogo.urls")),
    path("carrito/", include("carrito.urls")),
    path("pedidos/", include("pedidos.urls")),
    path("pruebas/", include("pruebas.urls")),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
