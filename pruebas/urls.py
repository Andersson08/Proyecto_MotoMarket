from django.urls import path

from . import views

app_name = "pruebas"

urlpatterns = [
    path("", views.mis_solicitudes, name="mis_solicitudes"),
    path("solicitar/<int:moto_id>/", views.solicitar, name="solicitar"),
]
