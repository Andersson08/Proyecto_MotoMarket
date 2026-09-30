from datetime import date

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from catalogo.models import Categoria, Marca
from catalogo.views import motos_visibles
from pedidos.models import DetallePedido, Pedido


def inicio(request):
    motos = motos_visibles()
    return render(
        request,
        "core/inicio.html",
        {
            "destacadas": motos.filter(destacada=True).order_by("-potencia_hp")[:6],
            "recientes": motos[:8],
            "marcas": Marca.objects.all(),
            "categorias": Categoria.objects.annotate(total=Count("motos")),
        },
    )


@staff_member_required
def reporte_ventas(request):
    hoy = date.today()
    desde = request.GET.get("desde") or hoy.replace(month=1, day=1).isoformat()
    hasta = request.GET.get("hasta") or hoy.isoformat()

    pedidos = Pedido.objects.filter(pago__estado="aprobado", fecha__date__range=(desde, hasta))
    detalles = DetallePedido.objects.filter(pedido__in=pedidos)
    return render(
        request,
        "core/reporte_ventas.html",
        {
            "desde": desde,
            "hasta": hasta,
            "resumen": pedidos.aggregate(ingresos=Sum("total"), cantidad=Count("id")),
            "unidades": detalles.aggregate(u=Sum("cantidad"))["u"] or 0,
            "por_mes": pedidos.annotate(mes=TruncMonth("fecha")).values("mes")
            .annotate(ingresos=Sum("total"), cantidad=Count("id")).order_by("mes"),
            "top_motos": detalles.values("moto__marca__nombre", "moto__modelo")
            .annotate(unidades=Sum("cantidad"), ingresos=Sum(F("cantidad") * F("precio_unitario")))
            .order_by("-unidades")[:10],
        },
    )
