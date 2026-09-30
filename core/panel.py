from datetime import date

from django.db.models import Sum
from django.urls import reverse

from catalogo.models import Moto
from pedidos.models import Pedido
from pruebas.models import SolicitudPrueba

POR_ATENDER = ["pagado", "en_preparacion"]


def pedidos_por_atender(request):
    return Pedido.objects.filter(estado__in=POR_ATENDER).count()


def pruebas_pendientes(request):
    return SolicitudPrueba.objects.filter(estado="pendiente").count()


def resumen(request, context):
    inicio_mes = date.today().replace(day=1)
    pagados_mes = Pedido.objects.filter(pago__estado="aprobado", fecha__date__gte=inicio_mes)
    poco_stock = Moto.objects.filter(activa=True, stock__lte=2).select_related("marca").order_by("stock")
    url_pedidos = reverse("admin:pedidos_pedido_changelist")
    url_pruebas = reverse("admin:pruebas_solicitudprueba_changelist")
    url_motos = reverse("admin:catalogo_moto_changelist")

    context.update(
        {
            "tarjetas": [
                {
                    "titulo": "Ventas del mes",
                    "valor": pagados_mes.aggregate(t=Sum("total"))["t"] or 0,
                    "dinero": True,
                    "detalle": f"{pagados_mes.count()} pedido(s) pagado(s)",
                    "icono": "payments",
                    "enlace": reverse("core:reporte_ventas"),
                },
                {
                    "titulo": "Pedidos por atender",
                    "valor": Pedido.objects.filter(estado__in=POR_ATENDER).count(),
                    "detalle": "Pagados o en preparación",
                    "icono": "local_shipping",
                    "enlace": f"{url_pedidos}?estado__in=pagado,en_preparacion",
                },
                {
                    "titulo": "Pruebas por aprobar",
                    "valor": SolicitudPrueba.objects.filter(estado="pendiente").count(),
                    "detalle": "Solicitudes de prueba de manejo",
                    "icono": "event_available",
                    "enlace": f"{url_pruebas}?estado__exact=pendiente",
                },
                {
                    "titulo": "Motos con poco stock",
                    "valor": poco_stock.count(),
                    "detalle": "2 unidades o menos",
                    "icono": "inventory_2",
                    "enlace": f"{url_motos}?stock__lte=2",
                },
            ],
            "accesos": [
                {"texto": "Agregar moto", "icono": "add_circle", "enlace": reverse("admin:catalogo_moto_add")},
                {"texto": "Ver pedidos", "icono": "receipt_long", "enlace": url_pedidos},
                {"texto": "Aprobar pruebas", "icono": "event_available", "enlace": f"{url_pruebas}?estado__exact=pendiente"},
                {"texto": "Reporte de ventas", "icono": "monitoring", "enlace": reverse("core:reporte_ventas")},
            ],
            "ultimos_pedidos": Pedido.objects.select_related("usuario")[:6],
            "pruebas": SolicitudPrueba.objects.filter(estado="pendiente").select_related("usuario", "moto__marca")[:6],
            "poco_stock": poco_stock[:6],
        }
    )
    return context
