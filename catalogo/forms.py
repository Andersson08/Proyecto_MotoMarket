from django import forms
from django.db.models import Q

from .models import Categoria, Marca, Moto, Resena


class FiltroMotosForm(forms.Form):
    ORDENES = [
        ("", "Más recientes"),
        ("precio", "Precio: menor a mayor"),
        ("-precio", "Precio: mayor a menor"),
        ("-cilindraje", "Mayor cilindraje"),
    ]

    q = forms.CharField(required=False, label="Buscar")
    marca = forms.ModelChoiceField(Marca.objects.all(), required=False, empty_label="Todas")
    categoria = forms.ModelChoiceField(
        Categoria.objects.all(), required=False, empty_label="Todas", label="Categoría"
    )
    combustible = forms.ChoiceField(
        choices=[("", "Todos")] + Moto.COMBUSTIBLES, required=False
    )
    precio_min = forms.IntegerField(required=False, min_value=0, label="Precio mínimo")
    precio_max = forms.IntegerField(required=False, min_value=0, label="Precio máximo")
    orden = forms.ChoiceField(choices=ORDENES, required=False)

    def filtrar(self, motos):
        if not self.is_valid():
            return motos
        d = self.cleaned_data
        if d["q"]:
            for palabra in d["q"].split():
                motos = motos.filter(
                    Q(modelo__icontains=palabra)
                    | Q(marca__nombre__icontains=palabra)
                    | Q(categoria__nombre__icontains=palabra)
                    | Q(descripcion__icontains=palabra)
                )
        if d["marca"]:
            motos = motos.filter(marca=d["marca"])
        if d["categoria"]:
            motos = motos.filter(categoria=d["categoria"])
        if d["combustible"]:
            motos = motos.filter(combustible=d["combustible"])
        if d["precio_min"] is not None:
            motos = motos.filter(precio__gte=d["precio_min"])
        if d["precio_max"] is not None:
            motos = motos.filter(precio__lte=d["precio_max"])
        if d["orden"]:
            motos = motos.order_by(d["orden"])
        return motos


class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ["calificacion", "comentario"]
        widgets = {
            "calificacion": forms.Select(choices=[(i, f"{i} ★") for i in range(5, 0, -1)]),
            "comentario": forms.Textarea(attrs={"rows": 3}),
        }
