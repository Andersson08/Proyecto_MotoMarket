from django.urls import path

from . import views

app_name = "carrito"

urlpatterns = [
    path("", views.ver, name="ver"),
    path("agregar/<int:moto_id>/", views.agregar, name="agregar"),
    path("actualizar/<int:item_id>/", views.actualizar, name="actualizar"),
    path("eliminar/<int:item_id>/", views.eliminar, name="eliminar"),
]
