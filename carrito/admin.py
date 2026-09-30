from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Carrito, ItemCarrito


class ItemCarritoInline(TabularInline):
    model = ItemCarrito
    extra = 0


@admin.register(Carrito)
class CarritoAdmin(ModelAdmin):
    list_display = ["usuario", "cantidad_items", "total", "actualizado"]
    inlines = [ItemCarritoInline]
