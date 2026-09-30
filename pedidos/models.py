import uuid

from django.conf import settings
from django.db import models

from catalogo.models import Moto


class Pedido(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente de pago"),
        ("pagado", "Pagado"),
        ("en_preparacion", "En preparación"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="pedidos"
    )
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    total = models.DecimalField(max_digits=14, decimal_places=0, default=0)
    direccion_entrega = models.CharField("dirección de entrega", max_length=200)
    ciudad = models.CharField(max_length=80)
    telefono = models.CharField("teléfono", max_length=20)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"Pedido #{self.pk}"

    @property
    def pagado(self):
        return hasattr(self, "pago") and self.pago.estado == "aprobado"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    moto = models.ForeignKey(Moto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=0)

    class Meta:
        verbose_name = "detalle de pedido"
        verbose_name_plural = "detalles de pedido"

    def __str__(self):
        return f"{self.cantidad} × {self.moto}"

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad


class Pago(models.Model):
    METODOS = [("tarjeta", "Tarjeta de crédito/débito"), ("pse", "PSE"), ("efectivo", "Efectivo en sede")]
    ESTADOS = [("aprobado", "Aprobado"), ("rechazado", "Rechazado")]

    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name="pago")
    metodo = models.CharField("método", max_length=20, choices=METODOS)
    monto = models.DecimalField(max_digits=14, decimal_places=0)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    referencia = models.CharField(max_length=40, unique=True, editable=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.referencia} ({self.get_estado_display()})"

    def save(self, *args, **kwargs):
        if not self.referencia:
            self.referencia = "MM-" + uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)
