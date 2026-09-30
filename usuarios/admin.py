from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ["username", "email", "first_name", "last_name", "ciudad", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active", "ciudad"]
    fieldsets = UserAdmin.fieldsets + (
        ("Datos de contacto", {"fields": ("documento", "telefono", "direccion", "ciudad", "acepta_datos")}),
    )
