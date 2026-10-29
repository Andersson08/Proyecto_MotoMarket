from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from catalogo.api import CategoriaViewSet, MarcaViewSet, MotoViewSet
from usuarios.api import CsrfView, LoginView, LogoutView, SesionView

router = DefaultRouter()
router.register("categorias", CategoriaViewSet, basename="categoria")
router.register("marcas", MarcaViewSet, basename="marca")
router.register("motos", MotoViewSet, basename="moto")

urlpatterns = [
    path("auth/csrf/", CsrfView.as_view(), name="auth-csrf"),
    path("auth/sesion/", SesionView.as_view(), name="auth-sesion"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/logout/", LogoutView.as_view(), name="auth-logout"),
    path("schema/",SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("", include(router.urls)),
]
