from django.urls import path

from . import views

app_name = "pedidos"

urlpatterns = [
    path("", views.mis_pedidos, name="mis_pedidos"),
    path("checkout/", views.checkout, name="checkout"),
    path("<int:pk>/", views.detalle, name="detalle"),
    path("<int:pk>/pagar/", views.pagar, name="pagar"),
    path("<int:pk>/cancelar/", views.cancelar, name="cancelar"),
]
