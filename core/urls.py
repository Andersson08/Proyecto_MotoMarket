from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "core"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("reportes/ventas/", views.reporte_ventas, name="reporte_ventas"),
    path("contacto/", TemplateView.as_view(template_name="core/contacto.html"), name="contacto"),
    path("preguntas-frecuentes/", TemplateView.as_view(template_name="core/preguntas.html"), name="preguntas"),
    path("terminos-y-condiciones/", TemplateView.as_view(template_name="core/terminos.html"), name="terminos"),
    path("politica-de-privacidad/", TemplateView.as_view(template_name="core/privacidad.html"), name="privacidad"),
]
