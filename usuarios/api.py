from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

UsuarioSerializer = inline_serializer(
    "SesionUsuario",
    {
        "autenticado": serializers.BooleanField(),
        "usuario": serializers.CharField(allow_null=True),
        "es_admin": serializers.BooleanField(),
    },
)


def datos_sesion(usuario):
    if not usuario.is_authenticated:
        return {"autenticado": False, "usuario": None, "es_admin": False}
    return {"autenticado": True, "usuario": usuario.get_username(), "es_admin": usuario.is_staff}


class LoginSerializer(serializers.Serializer):
    usuario = serializers.CharField()
    clave = serializers.CharField(style={"input_type": "password"})


@extend_schema(tags=["Sesión"])
class CsrfView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary="Obtener el token CSRF",
        description="Entrega el token que el frontend debe enviar en la cabecera X-CSRFToken "
        "en toda petición POST, PUT, PATCH o DELETE.",
        responses=inline_serializer("TokenCsrf", {"csrfToken": serializers.CharField()}),
    )
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({"csrfToken": get_token(request)})


@extend_schema(tags=["Sesión"])
class SesionView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(summary="Usuario de la sesión actual", responses=UsuarioSerializer)
    def get(self, request):
        return Response(datos_sesion(request.user))


@extend_schema(tags=["Sesión"])
@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary="Iniciar sesión",
        description="Recibe usuario (o correo) y clave. Exige la cabecera X-CSRFToken.",
        request=LoginSerializer,
        responses={200: UsuarioSerializer, 400: None, 403: None},
    )
    def post(self, request):
        datos = LoginSerializer(data=request.data)
        datos.is_valid(raise_exception=True)
        usuario = authenticate(
            request._request, username=datos.validated_data["usuario"], password=datos.validated_data["clave"]
        )
        if usuario is None:
            return Response(
                {"detail": "Usuario o clave incorrectos."}, status=status.HTTP_400_BAD_REQUEST
            )
        login(request._request, usuario)
        return Response(datos_sesion(usuario))


@extend_schema(tags=["Sesión"])
@method_decorator(csrf_protect, name="dispatch")
class LogoutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(summary="Cerrar sesión", request=None, responses=UsuarioSerializer)
    def post(self, request):
        logout(request._request)
        return Response(datos_sesion(request.user))
