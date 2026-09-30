from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import LoginForm, PerfilForm, RegistroForm


def registro(request):
    if request.user.is_authenticated:
        return redirect("core:inicio")
    form = RegistroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        login(request, usuario, backend="usuarios.backends.UsuarioOCorreoBackend")
        messages.success(request, f"¡Bienvenido a MotoMarket, {usuario.first_name}!")
        return redirect("core:inicio")
    return render(request, "usuarios/registro.html", {"form": form})


class IngresarView(LoginView):
    template_name = "usuarios/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


@login_required
def perfil(request):
    form = PerfilForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Tus datos se actualizaron.")
        return redirect("usuarios:perfil")
    return render(request, "usuarios/perfil.html", {"form": form})
