from datetime import date, time

from django import forms

from .models import SolicitudPrueba


class SolicitudPruebaForm(forms.ModelForm):
    class Meta:
        model = SolicitudPrueba
        fields = ["fecha", "hora", "licencia", "comentario"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "hora": forms.TimeInput(attrs={"type": "time"}),
            "comentario": forms.Textarea(attrs={"rows": 2}),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data["fecha"]
        if fecha <= date.today():
            raise forms.ValidationError("La prueba debe agendarse al menos para mañana.")
        if fecha.weekday() == 6:
            raise forms.ValidationError("Los domingos no hacemos pruebas de manejo.")
        return fecha

    def clean_hora(self):
        hora = self.cleaned_data["hora"]
        if not time(8, 0) <= hora <= time(17, 0):
            raise forms.ValidationError("El horario de pruebas es de 8:00 a. m. a 5:00 p. m.")
        return hora
