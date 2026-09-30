from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalogo.models import Moto

from .models import Carrito, ItemCarrito


def carrito_de(usuario):
    carrito, _ = Carrito.objects.get_or_create(usuario=usuario)
    return carrito


@login_required
def ver(request):
    carrito = carrito_de(request.user)
    items = carrito.items.select_related("moto__marca").prefetch_related("moto__imagenes")
    return render(request, "carrito/ver.html", {"carrito": carrito, "items": items})


@login_required
@require_POST
def agregar(request, moto_id):
    moto = get_object_or_404(Moto, pk=moto_id, activa=True)
    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito_de(request.user), moto=moto)
    nueva = 1 if creado else item.cantidad + 1
    if nueva > moto.stock:
        if creado:
            item.delete()
        messages.error(request, f"Solo hay {moto.stock} unidad(es) disponibles de {moto}.")
    else:
        item.cantidad = nueva
        item.save()
        messages.success(request, f"{moto} se agregó al carrito.")
    return redirect(request.POST.get("next") or "carrito:ver")


@login_required
@require_POST
def actualizar(request, item_id):
    item = get_object_or_404(ItemCarrito, pk=item_id, carrito__usuario=request.user)
    try:
        cantidad = int(request.POST.get("cantidad", 1))
    except ValueError:
        cantidad = item.cantidad
    if cantidad <= 0:
        item.delete()
    elif cantidad > item.moto.stock:
        messages.error(request, f"Solo hay {item.moto.stock} unidad(es) de {item.moto}.")
    else:
        item.cantidad = cantidad
        item.save()
    return redirect("carrito:ver")


@login_required
@require_POST
def eliminar(request, item_id):
    get_object_or_404(ItemCarrito, pk=item_id, carrito__usuario=request.user).delete()
    messages.info(request, "Moto eliminada del carrito.")
    return redirect("carrito:ver")
