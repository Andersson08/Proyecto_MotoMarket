from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import Usuario

admin.site.unregister(Group)


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ["username", "nombre_completo", "email", "telefono", "ciudad", "tipo", "is_active"]
    list_filter = ["is_staff", "is_active", "ciudad"]
    search_fields = ["username", "first_name", "last_name", "email", "documento", "telefono"]
    fieldsets = [
        ("Cuenta", {"fields": ["username", "password"]}),
        ("Datos personales", {"fields": ["first_name", "last_name", "email", "documento", "telefono", "direccion", "ciudad", "acepta_datos"]}),
        ("Permisos", {"fields": ["is_active", "is_staff", "is_superuser"], "description": "Marca \"Es staff\" para que la persona pueda entrar a este panel."}),
        ("Fechas", {"fields": ["last_login", "date_joined"]}),
    ]

    @display(description="Nombre")
    def nombre_completo(self, usuario):
        return usuario.get_full_name() or "—"

    @display(description="Tipo", label={"admin": "primary", "cliente": "info"})
    def tipo(self, usuario):
        return ("admin", "Administrador") if usuario.is_staff else ("cliente", "Cliente")
