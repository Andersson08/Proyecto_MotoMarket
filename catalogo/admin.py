from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display

from core.templatetags.moto_tags import cop

from .models import Categoria, ImagenMoto, Marca, Moto, Resena


class ImagenMotoInline(TabularInline):
    model = ImagenMoto
    extra = 0
    fields = ["vista_previa", "imagen", "url", "principal", "credito"]
    readonly_fields = ["vista_previa"]
    verbose_name = "foto"
    verbose_name_plural = "Fotos de la moto"

    @display(description="Vista previa")
    def vista_previa(self, imagen):
        return format_html('<img src="{}" style="height:70px;border-radius:8px">', imagen.src) if imagen.src else "—"


@admin.register(Moto)
class MotoAdmin(ModelAdmin):
    list_display = ["miniatura", "nombre", "categoria", "precio_cop", "stock_visible", "destacada", "activa"]
    list_display_links = ["miniatura", "nombre"]
    list_editable = ["destacada", "activa"]
    list_filter = ["marca", "categoria", "activa", "destacada", "combustible"]
    list_filter_submit = True
    search_fields = ["modelo", "marca__nombre", "descripcion"]
    list_per_page = 20
    readonly_fields = ["slug"]
    inlines = [ImagenMotoInline]
    fieldsets = [
        ("Información principal", {"fields": ["marca", "modelo", "categoria", "anio", "color", "descripcion"]}),
        ("Ficha técnica", {"fields": ["cilindraje", "potencia_hp", "combustible", "transmision"]}),
        ("Precio e inventario", {"fields": ["precio", "stock"]}),
        ("Publicación", {"fields": ["activa", "destacada", "slug"], "description": "Las motos destacadas salen en el carrusel de la página de inicio. Si desactivas una moto deja de verse en la tienda."}),
    ]

    @display(description="")
    def miniatura(self, moto):
        src = moto.imagen_pequena
        return format_html('<img src="{}" style="height:48px;width:72px;object-fit:contain">', src) if src else "—"

    @display(description="Moto", ordering="modelo")
    def nombre(self, moto):
        return str(moto)

    @display(description="Precio", ordering="precio")
    def precio_cop(self, moto):
        return cop(moto.precio)

    @display(description="Stock", ordering="stock", label={"Agotada": "danger", "Poco stock": "warning", "Disponible": "success"})
    def stock_visible(self, moto):
        if moto.stock == 0:
            return "Agotada", "Agotada"
        if moto.stock <= 2:
            return "Poco stock", f"Quedan {moto.stock}"
        return "Disponible", f"{moto.stock} unidades"


@admin.register(Marca)
class MarcaAdmin(ModelAdmin):
    list_display = ["nombre", "pais_origen", "cantidad_motos"]
    search_fields = ["nombre"]

    @display(description="Motos")
    def cantidad_motos(self, marca):
        return marca.motos.count()


@admin.register(Categoria)
class CategoriaAdmin(ModelAdmin):
    list_display = ["nombre", "descripcion", "cantidad_motos"]

    @display(description="Motos")
    def cantidad_motos(self, categoria):
        return categoria.motos.count()


@admin.register(Resena)
class ResenaAdmin(ModelAdmin):
    list_display = ["moto", "usuario", "estrellas", "comentario", "fecha"]
    list_filter = ["calificacion"]
    search_fields = ["moto__modelo", "usuario__username", "comentario"]

    @display(description="Calificación", ordering="calificacion")
    def estrellas(self, resena):
        return "★" * resena.calificacion + "☆" * (5 - resena.calificacion)
