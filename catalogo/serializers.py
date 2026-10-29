from django.utils.html import strip_tags
from rest_framework import serializers

from .models import Categoria, ImagenMoto, Marca, Moto


class SinHtmlMixin:
    def to_internal_value(self, data):
        valores = super().to_internal_value(data)
        for campo, valor in valores.items():
            if isinstance(valor, str):
                valores[campo] = strip_tags(valor).strip()
        return valores


class CategoriaSerializer(SinHtmlMixin, serializers.ModelSerializer):
    total_motos = serializers.IntegerField(read_only=True)

    class Meta:
        model = Categoria
        fields = ["id", "nombre", "descripcion", "total_motos"]


class MarcaSerializer(SinHtmlMixin, serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ["id", "nombre", "pais_origen"]


class MotoSerializer(SinHtmlMixin, serializers.ModelSerializer):
    marca_nombre = serializers.CharField(source="marca.nombre", read_only=True)
    categoria_nombre = serializers.CharField(source="categoria.nombre", read_only=True)
    imagen = serializers.SerializerMethodField()
    imagen_url = serializers.URLField(
        write_only=True,
        required=False,
        allow_blank=True,
        help_text="URL https de una foto de la moto (opcional).",
    )
    disponible = serializers.BooleanField(read_only=True)

    class Meta:
        model = Moto
        fields = [
            "id",
            "marca",
            "marca_nombre",
            "categoria",
            "categoria_nombre",
            "modelo",
            "slug",
            "anio",
            "cilindraje",
            "potencia_hp",
            "combustible",
            "transmision",
            "color",
            "precio",
            "stock",
            "descripcion",
            "destacada",
            "activa",
            "disponible",
            "imagen",
            "imagen_url",
        ]
        read_only_fields = ["slug"]

    def validate_imagen_url(self, valor):
        if valor and not valor.startswith("https://"):
            raise serializers.ValidationError("La imagen debe ser una URL https.")
        return valor

    def create(self, datos):
        imagen_url = datos.pop("imagen_url", "")
        moto = super().create(datos)
        if imagen_url:
            ImagenMoto.objects.create(moto=moto, url=imagen_url, principal=True)
        return moto

    def update(self, moto, datos):
        imagen_url = datos.pop("imagen_url", "")
        moto = super().update(moto, datos)
        if imagen_url:
            moto.imagenes.update(principal=False)
            ImagenMoto.objects.create(moto=moto, url=imagen_url, principal=True)
        return moto

    def get_imagen(self, moto) -> str:
        ruta = moto.imagen_pequena
        request = self.context.get("request")
        if ruta and request and not ruta.startswith("http"):
            return request.build_absolute_uri(ruta)
        return ruta
