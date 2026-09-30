from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.templatetags.static import static
from django.urls import reverse
from django.utils.text import slugify


class Marca(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    pais_origen = models.CharField("país de origen", max_length=60, blank=True)
    logo = models.ImageField(upload_to="marcas/", blank=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.TextField("descripción", blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.nombre


class Moto(models.Model):
    COMBUSTIBLES = [("gasolina", "Gasolina"), ("electrica", "Eléctrica")]
    TRANSMISIONES = [
        ("manual", "Manual"),
        ("automatica", "Automática"),
        ("semiautomatica", "Semiautomática"),
    ]

    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name="motos")
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="motos", verbose_name="categoría"
    )
    modelo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    anio = models.PositiveIntegerField("año")
    cilindraje = models.PositiveIntegerField("cilindraje (cc)", default=0)
    potencia_hp = models.DecimalField("potencia (HP)", max_digits=6, decimal_places=1, default=0)
    combustible = models.CharField(max_length=20, choices=COMBUSTIBLES, default="gasolina")
    transmision = models.CharField(
        "transmisión", max_length=20, choices=TRANSMISIONES, default="manual"
    )
    color = models.CharField(max_length=40, blank=True)
    precio = models.DecimalField("precio (COP)", max_digits=12, decimal_places=0)
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.TextField("descripción", blank=True)
    destacada = models.BooleanField(default=False)
    activa = models.BooleanField(default=True)
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creada"]

    def __str__(self):
        return f"{self.marca} {self.modelo} {self.anio}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.marca.nombre}-{self.modelo}-{self.anio}")
            slug, n = base, 2
            while Moto.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug, n = f"{base}-{n}", n + 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalogo:detalle", args=[self.slug])

    def _imagen(self):
        imagenes = list(self.imagenes.all())
        return next((i for i in imagenes if i.principal), imagenes[0] if imagenes else None)

    @property
    def imagen_principal(self):
        img = self._imagen()
        return img.src if img else ""

    @property
    def imagen_pequena(self):
        img = self._imagen()
        return img.src_pequena if img else ""

    @property
    def calificacion(self):
        return self.resenas.aggregate(p=Avg("calificacion"))["p"]

    @property
    def disponible(self):
        return self.activa and self.stock > 0


class ImagenMoto(models.Model):
    moto = models.ForeignKey(Moto, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to="motos/", blank=True)
    url = models.CharField("URL de la imagen", max_length=500, blank=True)
    credito = models.CharField("crédito de la foto", max_length=200, blank=True)
    principal = models.BooleanField(default=False)

    class Meta:
        verbose_name = "imagen de moto"
        verbose_name_plural = "imágenes de motos"

    def __str__(self):
        return f"Imagen de {self.moto}"

    @property
    def src(self):
        if self.imagen:
            return self.imagen.url
        if self.url and not self.url.startswith(("http", "/")):
            return static(self.url)
        return self.url

    @property
    def src_pequena(self):
        if not self.imagen and self.url.endswith(".webp") and not self.url.startswith(("http", "/")):
            pequena = self.url.replace(".webp", "-sm.webp")
            if staticfiles_storage.exists(pequena) or finders.find(pequena):
                return static(pequena)
        return self.src


class Resena(models.Model):
    moto = models.ForeignKey(Moto, on_delete=models.CASCADE, related_name="resenas")
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resenas"
    )
    calificacion = models.PositiveSmallIntegerField(
        "calificación", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "reseña"
        verbose_name_plural = "reseñas"
        constraints = [
            models.UniqueConstraint(fields=["moto", "usuario"], name="una_resena_por_moto")
        ]

    def __str__(self):
        return f"{self.usuario} → {self.moto} ({self.calificacion}★)"
