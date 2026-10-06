from rest_framework import serializers

from .models import Categoria, Marca, Moto


class CategoriaSerializer(serializers.ModelSerializer):
    total_motos = serializers.IntegerField(read_only=True)

    class Meta:
        model = Categoria
        fields = ["id", "nombre", "descripcion", "total_motos"]


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ["id", "nombre", "pais_origen"]


class MotoSerializer(serializers.ModelSerializer):
    marca_nombre = serializers.CharField(source="marca.nombre", read_only=True)
    categoria_nombre = serializers.CharField(source="categoria.nombre", read_only=True)
    imagen = serializers.SerializerMethodField()
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
        ]
        read_only_fields = ["slug"]

    def get_imagen(self, moto) -> str:
        ruta = moto.imagen_pequena
        request = self.context.get("request")
        if ruta and request and not ruta.startswith("http"):
            return request.build_absolute_uri(ruta)
        return ruta
