from django import forms

from .models import Pago, Pedido


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["direccion_entrega", "ciudad", "telefono", "notas"]
        widgets = {"notas": forms.Textarea(attrs={"rows": 2})}


class PagoForm(forms.Form):
    metodo = forms.ChoiceField(choices=Pago.METODOS, widget=forms.RadioSelect, label="Método de pago")
    titular = forms.CharField(required=False, max_length=80)
    numero_tarjeta = forms.CharField(required=False, max_length=19, label="Número de tarjeta")
    vencimiento = forms.CharField(required=False, max_length=5, label="Vencimiento (MM/AA)")
    cvv = forms.CharField(required=False, max_length=4, label="CVV")

    def clean(self):
        datos = super().clean()
        if datos.get("metodo") == "tarjeta":
            numero = (datos.get("numero_tarjeta") or "").replace(" ", "").replace("-", "")
            if not (numero.isdigit() and 13 <= len(numero) <= 19):
                self.add_error("numero_tarjeta", "Ingresa un número de tarjeta válido.")
            if not datos.get("titular"):
                self.add_error("titular", "Ingresa el nombre del titular.")
            if not (datos.get("cvv") or "").isdigit():
                self.add_error("cvv", "CVV inválido.")
            datos["numero_tarjeta"] = numero
        return datos

    def aprobado(self):
        d = self.cleaned_data
        return not (d["metodo"] == "tarjeta" and d["numero_tarjeta"].endswith("0000"))
