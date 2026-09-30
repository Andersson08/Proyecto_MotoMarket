from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    email = models.EmailField("correo electrónico", unique=True)
    documento = models.CharField("documento de identidad", max_length=20, blank=True)
    telefono = models.CharField("teléfono", max_length=20, blank=True)
    direccion = models.CharField("dirección", max_length=200, blank=True)
    ciudad = models.CharField(max_length=80, blank=True)
    acepta_datos = models.BooleanField(
        "acepta tratamiento de datos (Ley 1581 de 2012)", default=False
    )

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def __str__(self):
        return self.get_full_name() or self.username
