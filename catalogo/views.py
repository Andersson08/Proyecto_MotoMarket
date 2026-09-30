from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from pedidos.models import DetallePedido

from .forms import FiltroMotosForm, ResenaForm
from .models import Moto


def motos_visibles():
    return Moto.objects.filter(activa=True).select_related("marca", "categoria").prefetch_related("imagenes")


def lista(request):
    form = FiltroMotosForm(request.GET or None)
    motos = form.filtrar(motos_visibles())
    pagina = Paginator(motos, 12).get_page(request.GET.get("page"))
    parametros = request.GET.copy()
    parametros.pop("page", None)
    return render(
        request,
        "catalogo/lista.html",
        {"form": form, "pagina": pagina, "motos": pagina.object_list, "parametros": parametros.urlencode()},
    )


def puede_resenar(usuario, moto):
    if not usuario.is_authenticated or moto.resenas.filter(usuario=usuario).exists():
        return False
    return DetallePedido.objects.filter(
        pedido__usuario=usuario, pedido__pago__estado="aprobado", moto=moto
    ).exists()


def detalle(request, slug):
    moto = get_object_or_404(motos_visibles(), slug=slug)
    relacionadas = motos_visibles().filter(categoria=moto.categoria).exclude(pk=moto.pk)[:4]
    return render(
        request,
        "catalogo/detalle.html",
        {
            "moto": moto,
            "resenas": moto.resenas.select_related("usuario"),
            "relacionadas": relacionadas,
            "resena_form": ResenaForm() if puede_resenar(request.user, moto) else None,
        },
    )


@login_required
@require_POST
def resenar(request, slug):
    moto = get_object_or_404(motos_visibles(), slug=slug)
    if not puede_resenar(request.user, moto):
        messages.error(request, "Solo puedes reseñar motos que hayas comprado, y una sola vez.")
        return redirect(moto)
    form = ResenaForm(request.POST)
    if form.is_valid():
        resena = form.save(commit=False)
        resena.moto, resena.usuario = moto, request.user
        resena.save()
        messages.success(request, "¡Gracias por tu reseña!")
    else:
        messages.error(request, "Revisa la calificación e inténtalo de nuevo.")
    return redirect(moto)
