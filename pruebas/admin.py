from django.contrib import admin, messages
from unfold.admin import ModelAdmin
from unfold.decorators import action, display

from .models import SolicitudPrueba


@admin.register(SolicitudPrueba)
class SolicitudPruebaAdmin(ModelAdmin):
    list_display = ["usuario", "moto", "fecha", "hora", "telefono_cliente", "estado_visible"]
    list_filter = ["estado", "fecha"]
    list_filter_submit = True
    search_fields = ["usuario__username", "usuario__first_name", "moto__modelo"]
    list_per_page = 20
    readonly_fields = ["usuario", "moto", "fecha", "hora", "licencia", "comentario", "creada"]
    fieldsets = [
        ("Respuesta del concesionario", {"fields": ["estado", "respuesta_admin"], "description": "El cliente verá el estado y tu respuesta en \"Mis pruebas de manejo\"."}),
        ("Solicitud", {"fields": ["usuario", "moto", "fecha", "hora", "licencia", "comentario", "creada"]}),
    ]
    actions = ["aprobar", "rechazar", "marcar_realizada"]

    @display(description="Teléfono")
    def telefono_cliente(self, solicitud):
        return solicitud.usuario.telefono or "—"

    @display(
        description="Estado",
        ordering="estado",
        label={"pendiente": "warning", "aprobada": "success", "rechazada": "danger", "realizada": "primary"},
    )
    def estado_visible(self, solicitud):
        return solicitud.estado, solicitud.get_estado_display()

    @action(description="✅ Aprobar")
    def aprobar(self, request, queryset):
        messages.success(request, f"{queryset.update(estado='aprobada')} prueba(s) aprobada(s).")

    @action(description="❌ Rechazar")
    def rechazar(self, request, queryset):
        messages.success(request, f"{queryset.update(estado='rechazada')} prueba(s) rechazada(s).")

    @action(description="🏁 Marcar como realizada")
    def marcar_realizada(self, request, queryset):
        messages.success(request, f"{queryset.update(estado='realizada')} prueba(s) marcada(s) como realizada(s).")

    def has_add_permission(self, request):
        return False
