from django.contrib import admin, messages
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.decorators import action, display

from core.templatetags.moto_tags import cop

from .models import DetallePedido, Pago, Pedido

COLORES_PEDIDO = {
    "pendiente": "warning",
    "pagado": "success",
    "en_preparacion": "info",
    "entregado": "primary",
    "cancelado": "danger",
}


class DetallePedidoInline(TabularInline):
    model = DetallePedido
    extra = 0
    fields = ["moto", "cantidad", "precio_unitario"]
    readonly_fields = fields
    can_delete = False
    verbose_name_plural = "Motos del pedido"

    def has_add_permission(self, request, obj=None):
        return False


class PagoInline(StackedInline):
    model = Pago
    extra = 0
    fields = ["metodo", "monto", "estado", "referencia", "fecha"]
    readonly_fields = fields
    can_delete = False
    verbose_name_plural = "Pago"

    def has_add_permission(self, request, obj=None):
        return False


def cambiar_estado(request, queryset, estado, texto):
    cantidad = queryset.exclude(estado__in=["pendiente", "cancelado"]).update(estado=estado)
    if cantidad:
        messages.success(request, f"{cantidad} pedido(s) marcados como {texto}.")
    else:
        messages.warning(request, "Solo se cambian pedidos que ya estén pagados.")


@admin.register(Pedido)
class PedidoAdmin(ModelAdmin):
    list_display = ["__str__", "usuario", "fecha", "total_cop", "estado_visible", "ciudad"]
    list_filter = ["estado", "fecha", "ciudad"]
    list_filter_submit = True
    search_fields = ["usuario__username", "usuario__email", "usuario__first_name", "id"]
    date_hierarchy = "fecha"
    list_per_page = 20
    inlines = [DetallePedidoInline, PagoInline]
    readonly_fields = ["usuario", "fecha", "total"]
    fieldsets = [
        ("Estado del pedido", {"fields": ["estado"], "description": "Cambia el estado a medida que alistas y entregas la moto."}),
        ("Cliente y entrega", {"fields": ["usuario", "direccion_entrega", "ciudad", "telefono", "notas"]}),
        ("Resumen", {"fields": ["fecha", "total"]}),
    ]
    actions = ["marcar_en_preparacion", "marcar_entregado"]

    @display(description="Total", ordering="total")
    def total_cop(self, pedido):
        return cop(pedido.total)

    @display(description="Estado", ordering="estado", label=COLORES_PEDIDO)
    def estado_visible(self, pedido):
        return pedido.estado, pedido.get_estado_display()

    @action(description="Marcar como en preparación")
    def marcar_en_preparacion(self, request, queryset):
        cambiar_estado(request, queryset, "en_preparacion", "en preparación")

    @action(description="Marcar como entregado")
    def marcar_entregado(self, request, queryset):
        cambiar_estado(request, queryset, "entregado", "entregados")

    def has_add_permission(self, request):
        return False


@admin.register(Pago)
class PagoAdmin(ModelAdmin):
    list_display = ["referencia", "pedido", "metodo", "monto_cop", "estado_visible", "fecha"]
    list_filter = ["estado", "metodo", "fecha"]
    search_fields = ["referencia", "pedido__usuario__username"]
    readonly_fields = ["pedido", "metodo", "monto", "estado", "referencia", "fecha"]

    @display(description="Monto", ordering="monto")
    def monto_cop(self, pago):
        return cop(pago.monto)

    @display(description="Estado", ordering="estado", label={"aprobado": "success", "rechazado": "danger"})
    def estado_visible(self, pago):
        return pago.estado, pago.get_estado_display()

    def has_add_permission(self, request):
        return False
