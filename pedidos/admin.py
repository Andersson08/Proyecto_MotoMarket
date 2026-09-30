from django.contrib import admin

from .models import DetallePedido, Pago, Pedido


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ["moto", "cantidad", "precio_unitario"]
    can_delete = False


class PagoInline(admin.StackedInline):
    model = Pago
    extra = 0
    readonly_fields = ["metodo", "monto", "estado", "referencia", "fecha"]
    can_delete = False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["__str__", "usuario", "fecha", "total", "estado"]
    list_editable = ["estado"]
    list_filter = ["estado", "fecha", "ciudad"]
    search_fields = ["usuario__username", "usuario__email", "pk"]
    date_hierarchy = "fecha"
    inlines = [DetallePedidoInline, PagoInline]


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ["referencia", "pedido", "metodo", "monto", "estado", "fecha"]
    list_filter = ["estado", "metodo"]
