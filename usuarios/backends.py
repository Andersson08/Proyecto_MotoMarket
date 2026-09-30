from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class UsuarioOCorreoBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username and "@" in username:
            usuario = get_user_model().objects.filter(email__iexact=username).first()
            if usuario:
                username = usuario.username
        return super().authenticate(request, username=username, password=password, **kwargs)
