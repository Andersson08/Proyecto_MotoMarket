from django.contrib import admin
from django.utils.html import format_html

from .models import Categoria, ImagenMoto, Marca, Moto, Resena


class ImagenMotoInline(admin.TabularInline):
    model = ImagenMoto
    extra = 1


@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    list_display = ["miniatura", "__str__", "categoria", "cilindraje", "precio", "stock", "destacada", "activa"]
    list_display_links = ["miniatura", "__str__"]
    list_editable = ["precio", "stock", "destacada", "activa"]
    list_filter = ["marca", "categoria", "combustible", "activa", "destacada"]
    search_fields = ["modelo", "marca__nombre", "descripcion"]
    readonly_fields = ["slug"]
    inlines = [ImagenMotoInline]

    @admin.display(description="")
    def miniatura(self, moto):
        src = moto.imagen_principal
        return format_html('<img src="{}" style="height:40px">', src) if src else "—"


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "pais_origen"]
    search_fields = ["nombre"]


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "descripcion"]


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ["moto", "usuario", "calificacion", "fecha"]
    list_filter = ["calificacion"]
