from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from catalogo.models import Moto

from .forms import SolicitudPruebaForm


@login_required
def solicitar(request, moto_id):
    moto = get_object_or_404(Moto, pk=moto_id, activa=True)
    form = SolicitudPruebaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        solicitud = form.save(commit=False)
        solicitud.usuario, solicitud.moto = request.user, moto
        solicitud.save()
        messages.success(request, "Recibimos tu solicitud. Te avisaremos cuando el concesionario la apruebe.")
        return redirect("pruebas:mis_solicitudes")
    return render(request, "pruebas/solicitar.html", {"form": form, "moto": moto})


@login_required
def mis_solicitudes(request):
    solicitudes = request.user.solicitudes_prueba.select_related("moto__marca")
    return render(request, "pruebas/mis_solicitudes.html", {"solicitudes": solicitudes})
