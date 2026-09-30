from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Usuario


class RegistroForm(UserCreationForm):
    acepta_datos = forms.BooleanField(
        required=True,
        label="Autorizo el tratamiento de mis datos personales (Ley 1581 de 2012)",
    )

    class Meta:
        model = Usuario
        fields = ["username", "first_name", "last_name", "email", "telefono", "ciudad", "acepta_datos"]
        labels = {"username": "Usuario", "first_name": "Nombres", "last_name": "Apellidos"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("first_name", "last_name", "email"):
            self.fields[name].required = True


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario o correo")


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["first_name", "last_name", "email", "documento", "telefono", "direccion", "ciudad"]
        labels = {"first_name": "Nombres", "last_name": "Apellidos"}
