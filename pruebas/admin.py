from django.contrib import admin

from .models import SolicitudPrueba


@admin.register(SolicitudPrueba)
class SolicitudPruebaAdmin(admin.ModelAdmin):
    list_display = ["usuario", "moto", "fecha", "hora", "estado"]
    list_editable = ["estado"]
    list_filter = ["estado", "fecha"]
    search_fields = ["usuario__username", "moto__modelo"]
    actions = ["aprobar", "rechazar", "marcar_realizada"]

    @admin.action(description="Aprobar solicitudes seleccionadas")
    def aprobar(self, request, queryset):
        queryset.update(estado="aprobada")

    @admin.action(description="Rechazar solicitudes seleccionadas")
    def rechazar(self, request, queryset):
        queryset.update(estado="rechazada")

    @admin.action(description="Marcar como realizadas")
    def marcar_realizada(self, request, queryset):
        queryset.update(estado="realizada")
