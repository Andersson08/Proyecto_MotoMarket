from django.conf import settings
from django.db import models

from catalogo.models import Moto


class SolicitudPrueba(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("aprobada", "Aprobada"),
        ("rechazada", "Rechazada"),
        ("realizada", "Realizada"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="solicitudes_prueba"
    )
    moto = models.ForeignKey(Moto, on_delete=models.CASCADE, related_name="solicitudes_prueba")
    fecha = models.DateField("fecha deseada")
    hora = models.TimeField("hora deseada")
    licencia = models.CharField("número de licencia de conducción", max_length=30)
    comentario = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    respuesta_admin = models.TextField("respuesta del concesionario", blank=True)
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creada"]
        verbose_name = "solicitud de prueba de manejo"
        verbose_name_plural = "solicitudes de prueba de manejo"

    def __str__(self):
        return f"{self.usuario} – {self.moto} ({self.fecha})"
