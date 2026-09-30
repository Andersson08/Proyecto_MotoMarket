from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path("ingresar/", views.IngresarView.as_view(), name="login"),
    path("salir/", LogoutView.as_view(), name="logout"),
    path("perfil/", views.perfil, name="perfil"),
]
