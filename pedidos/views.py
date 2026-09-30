from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from carrito.views import carrito_de
from catalogo.models import Moto

from .forms import CheckoutForm, PagoForm
from .models import DetallePedido, Pago, Pedido


def falta_stock(items):
    return [i for i in items if i.cantidad > i.moto.stock or not i.moto.activa]


@login_required
def checkout(request):
    carrito = carrito_de(request.user)
    items = list(carrito.items.select_related("moto__marca"))
    if not items:
        messages.info(request, "Tu carrito está vacío.")
        return redirect("catalogo:lista")
    faltantes = falta_stock(items)
    if faltantes:
        messages.error(request, f"No hay suficientes unidades de {faltantes[0].moto}. Ajusta tu carrito.")
        return redirect("carrito:ver")

    u = request.user
    form = CheckoutForm(
        request.POST or None,
        initial={"direccion_entrega": u.direccion, "ciudad": u.ciudad, "telefono": u.telefono},
    )
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            pedido = form.save(commit=False)
            pedido.usuario = u
            pedido.total = sum(i.subtotal for i in items)
            pedido.save()
            DetallePedido.objects.bulk_create(
                DetallePedido(pedido=pedido, moto=i.moto, cantidad=i.cantidad, precio_unitario=i.moto.precio)
                for i in items
            )
            carrito.items.all().delete()
        return redirect("pedidos:pagar", pedido.pk)
    return render(
        request,
        "pedidos/checkout.html",
        {"form": form, "items": items, "total": sum(i.subtotal for i in items)},
    )


@login_required
def pagar(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk, usuario=request.user)
    if pedido.estado != "pendiente":
        return redirect("pedidos:detalle", pk)
    form = PagoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            detalles = list(pedido.detalles.select_related("moto"))
            motos = {m.pk: m for m in Moto.objects.select_for_update().filter(pk__in=[d.moto_id for d in detalles])}
            sin_stock = [d for d in detalles if d.cantidad > motos[d.moto_id].stock]
            if sin_stock:
                messages.error(request, f"Lo sentimos, ya no hay unidades suficientes de {sin_stock[0].moto}.")
                return redirect("pedidos:detalle", pk)
            aprobado = form.aprobado()
            Pago.objects.update_or_create(
                pedido=pedido,
                defaults={
                    "metodo": form.cleaned_data["metodo"],
                    "monto": pedido.total,
                    "estado": "aprobado" if aprobado else "rechazado",
                },
            )
            if aprobado:
                for d in detalles:
                    moto = motos[d.moto_id]
                    moto.stock -= d.cantidad
                    moto.save(update_fields=["stock"])
                pedido.estado = "pagado"
                pedido.save(update_fields=["estado"])
        if aprobado:
            messages.success(request, "¡Pago aprobado! Tu pedido quedó confirmado.")
            return redirect("pedidos:detalle", pk)
        messages.error(request, "El pago fue rechazado por el banco (simulado). Intenta con otro medio.")
        return redirect("pedidos:pagar", pk)
    return render(request, "pedidos/pagar.html", {"pedido": pedido, "form": form})


@login_required
def mis_pedidos(request):
    pedidos = request.user.pedidos.prefetch_related("detalles__moto")
    return render(request, "pedidos/mis_pedidos.html", {"pedidos": pedidos})


@login_required
def detalle(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.prefetch_related("detalles__moto__imagenes"), pk=pk, usuario=request.user
    )
    return render(request, "pedidos/detalle.html", {"pedido": pedido})


@login_required
@require_POST
def cancelar(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk, usuario=request.user)
    if pedido.estado == "pendiente":
        pedido.estado = "cancelado"
        pedido.save(update_fields=["estado"])
        messages.info(request, f"{pedido} fue cancelado.")
    else:
        messages.error(request, "Solo se pueden cancelar pedidos pendientes de pago.")
    return redirect("pedidos:detalle", pk)
