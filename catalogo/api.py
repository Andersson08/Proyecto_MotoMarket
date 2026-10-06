from django.db.models import Count, ProtectedError, Q
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import Categoria, Marca, Moto
from .serializers import CategoriaSerializer, MarcaSerializer, MotoSerializer


class LecturaPublicaEscrituraAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class EliminacionProtegidaMixin:
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"detail": "No se puede eliminar porque tiene registros asociados."},
                status=status.HTTP_409_CONFLICT,
            )


@extend_schema(tags=["Categorías"])
class CategoriaViewSet(EliminacionProtegidaMixin, viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    permission_classes = [LecturaPublicaEscrituraAdmin]

    def get_queryset(self):
        return Categoria.objects.annotate(
            total_motos=Count("motos", filter=Q(motos__activa=True))
        )


@extend_schema(tags=["Marcas"])
class MarcaViewSet(EliminacionProtegidaMixin, viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [LecturaPublicaEscrituraAdmin]


@extend_schema(tags=["Productos (motos)"])
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("categoria", int, description="Id de la categoría"),
            OpenApiParameter("marca", int, description="Id de la marca"),
            OpenApiParameter("buscar", str, description="Texto en el modelo o la marca"),
        ]
    )
)
class MotoViewSet(EliminacionProtegidaMixin, viewsets.ModelViewSet):
    serializer_class = MotoSerializer
    permission_classes = [LecturaPublicaEscrituraAdmin]

    def get_queryset(self):
        motos = Moto.objects.select_related("marca", "categoria").prefetch_related("imagenes")
        if not self.request.user.is_staff:
            motos = motos.filter(activa=True)
        if self.action != "list":
            return motos
        parametros = self.request.query_params
        if parametros.get("categoria", "").isdigit():
            motos = motos.filter(categoria_id=parametros["categoria"])
        if parametros.get("marca", "").isdigit():
            motos = motos.filter(marca_id=parametros["marca"])
        if parametros.get("buscar"):
            texto = parametros["buscar"]
            motos = motos.filter(Q(modelo__icontains=texto) | Q(marca__nombre__icontains=texto))
        return motos
