from django.conf import settings
from django.db import models

from catalogo.models import Moto


class Carrito(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="carrito"
    )
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.usuario}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.select_related("moto"))

    @property
    def cantidad_items(self):
        return sum(item.cantidad for item in self.items.all())


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    moto = models.ForeignKey(Moto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "ítem del carrito"
        verbose_name_plural = "ítems del carrito"
        constraints = [
            models.UniqueConstraint(fields=["carrito", "moto"], name="moto_unica_en_carrito")
        ]

    def __str__(self):
        return f"{self.cantidad} × {self.moto}"

    @property
    def subtotal(self):
        return self.moto.precio * self.cantidad
